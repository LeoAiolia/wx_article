---
title: 告别单 Window 时代：UIKit Scene 生命周期的架构演进与迁移实战
cover: ../assets/cover-uikit-scene-lifecycle.png
---

# 告别单 Window 时代：UIKit Scene 生命周期的架构演进与迁移实战

> 苹果官方合规倒计时：从原理到 iOS 原生及 Flutter 混合工程的 Scene 架构迁移指南。

---

## 前言

在 iOS 13 之前，无论是启动 App、处理后台切换、响应推送跳转，还是在屏幕上显示 UI，我们都习惯于直接在 `AppDelegate` 中操作 `self.window`。整个应用程序建立在“单个应用程序只有一个 UI 窗体”的默认假设上。

然而，随着 iPadOS 的独立、多窗口与 Slide Over/Split View 的引入，以及 iOS 16+ 的 Stage Manager（舞台调度）和 visionOS 空间计算的兴起，苹果对 UIKit 底层架构进行了深刻的重构——全面推行场景化生命周期 (`UIScene` 与 `UISceneDelegate`)。

> **⚠️ 苹果强制合规警告（附官方时间线）**
>
> 苹果在官方文档 [Transitioning to the UIKit Scene-based Life Cycle](https://developer.apple.com/documentation/UIKit/transitioning-to-the-uikit-scene-based-life-cycle) 与 [Specifying the Scenes Your App Supports](https://developer.apple.com/documentation/uikit/specifying-the-scenes-your-app-supports) 中给出了明确的强制时间表，Scene-based 生命周期已从“推荐实践”变为**运行时硬性要求**：
>
> * **iOS 18.4 起**：未适配的 App 启动时打印警告日志 `This process does not adopt UIScene lifecycle. This will become an assert in a future version.`
> * **iOS 26 起**：警告升级为 `UIScene lifecycle will soon be required. Failure to adopt will result in an assert in the future.`
> * **iOS 27 起（2026 年秋季）**：官方原文明确声明——使用最新 SDK 构建的 App 必须采用 Scene 生命周期，**否则将直接无法启动**（fail to launch）。
>
> 不仅原生 iOS 项目需要完成适配，**所有基于 Flutter / React Native 等跨平台框架构建的 App，也必须在宿主工程中迁移支持 Scene**。距离 iOS 27 正式发布仅剩数月，尚未迁移的项目已进入真正的合规倒计时。

本文将从场景化演进的底层设计出发，厘清 `UIApplicationDelegate` 与 `UISceneDelegate` 的分工，详解 `Info.plist` 中的 `UIApplicationSceneManifest` 配置，并分别针对 **iOS 原生应用** 与 **Flutter 移动应用** 提供生产级迁移方案及踩坑防护策略。

---

## 一、架构变迁：进程生命周期与 UI 实例生命周期的解耦

### 1. 传统的 App 生命周期（iOS 12 及以前）

在传统架构中，`UIApplicationDelegate` 既管理进程状态，又控制界面渲染：
* `application(_:didFinishLaunchingWithOptions:)` 负责进程初始化并创建 `self.window`。
* `applicationDidEnterBackground(_:)` 与 `applicationDidBecomeActive(_:)` 同时承担系统进程事件与 UI 显隐逻辑。

这种设计的致命缺点在于：**严重违背单一职责原则（Single Responsibility Principle）**。一旦系统支持同时打开多个独立窗口（例如 iPadOS 上的两个 Word 文档窗口、两个 Safari 页面），单个 `window` 属性和全局的 UI 回调便彻底失效。

### 2. Scene-based 现代架构（iOS 13 及以后）

为了支持一个 App 拥有多个独立的 UI 界面实例，苹果将生命周期剥离为两个层面：

1. **进程生命周期（Process Life Cycle）**：由 `UIApplicationDelegate` 统一负责。
   * 关注 App 进程的启动、终止、内存警告、推送 Token 注册、全局 SDK 初始化等与系统进程强相关的事务。
2. **UI 实例生命周期（UI Life Cycle）**：由 `UISceneDelegate`（具体为 `UIWindowSceneDelegate`）分管。
   * 每个窗口（`UIScene`）拥有独立的生命周期和状态（Foreground Active、Foreground Inactive、Background、Unattached）。
   * 负责窗口创建、`rootViewController` 挂载、界面前后台切换、用户交互事件等。

### 3. 回调函数映射表

下表梳理了传统 `AppDelegate` 与现代 `SceneDelegate` 的回调对应关系：

| 传统 AppDelegate 回调 (iOS 12前) | 现代 SceneDelegate 对应回调 (iOS 13+) | 职责定位 |
|---|---|---|
| `application(_:didFinishLaunchingWithOptions:)` | `scene(_:willConnectTo:options:)` | 界面初始化与 `UIWindow` 挂载 |
| `applicationDidBecomeActive(_:)` | `sceneDidBecomeActive(_:)` | 界面进入活跃状态，恢复 UI 定时器/动画 |
| `applicationWillResignActive(_:)` | `sceneWillResignActive(_:)` | 界面即将失去焦点，暂停 UI 任务 |
| `applicationDidEnterBackground(_:)` | `sceneDidEnterBackground(_:)` | 界面退至后台，保存 UI 状态/持久化草稿 |
| `applicationWillEnterForeground(_:)` | `sceneWillEnterForeground(_:)` | 界面即将从后台返回前台，刷新 UI 数据 |
| (无对应，旧架构由系统销毁进程) | `sceneDidDisconnect(_:)` | 场景被系统或用户主动销毁，释放窗口资源 |

---

## 二、配置清单：如何在 Info.plist 中声明 Scene 支持

支持 Scene 架构的前提是在工程配置中正确声明 `UIApplicationSceneManifest`（即 `Application Scene Manifest`）。

### 1. 节点结构解析

在 `Info.plist`（或 Xcode 的 Target Info 配置面板）中，需要包含以下配置项：

```xml
<key>UIApplicationSceneManifest</key>
<dict>
    <!-- 是否支持多窗口机制（iPadOS / visionOS 开启；纯 iPhone 应用可设为 NO，但仍必须保持 Scene 架构配置） -->
    <key>UIApplicationSupportsMultipleScenes</key>
    <false/>
    <!-- 定义 App 支持的 Scene 配置集合 -->
    <key>UISceneConfigurations</key>
    <dict>
        <!-- 主应用程序角色配置（Standard Application Scenes） -->
        <key>UIWindowSceneSessionRoleApplication</key>
        <array>
            <dict>
                <!-- 场景配置名称，可用于代码中指定 Scene 启动 -->
                <key>UISceneConfigurationName</key>
                <string>Default Configuration</string>
                <!-- 绑定的 Delegate 类名 -->
                <key>UISceneDelegateClassName</key>
                <string>$(PRODUCT_MODULE_NAME).SceneDelegate</string>
                <!-- 如果使用 Storyboard，在此配置 Storyboard 名称；纯代码项目保持不填或移除 -->
                <!-- <key>UISceneStoryboardFile</key>
                <string>Main</string> -->
            </dict>
        </array>
    </dict>
</dict>
```

### 2. AppDelegate 中响应场景注册

当系统需要新建 Scene 时，会调用 `UIApplicationDelegate` 的回调询问具体配置：

```swift
func application(
    _ application: UIApplication,
    configurationForConnecting connectingSceneSession: UISceneSession,
    options: UIScene.ConnectionOptions
) -> UISceneConfiguration {
    // 根据 connectingSceneSession.role 选择对应的配置名称
    return UISceneConfiguration(
        name: "Default Configuration",
        sessionRole: connectingSceneSession.role
    )
}

func application(
    _ application: UIApplication,
    didDiscardSceneSessions sceneSessions: Set<UISceneSession>
) {
    // 当用户在多任务切换器中主动划掉某个 Scene 时触发
    // 可在此清理该 Scene 持有且未保存的临时资源
}
```

---

## 三、iOS 原生工程实战迁移：平构重构三步法

针对一个原本依赖 `AppDelegate` 的传统 iOS 原生工程，我们可以按以下步骤进行平滑重构。

### 步骤 1：纯代码 UI 工程中创建并初始化 `SceneDelegate`

新建 `SceneDelegate.swift`，继承自 `UIResponder` 并实现 `UIWindowSceneDelegate` 协议：

```swift
import UIKit

final class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    
    var window: UIWindow?
    
    func scene(
        _ scene: UIScene,
        willConnectTo session: UISceneSession,
        options connectionOptions: UIScene.ConnectionOptions
    ) {
        // 1. 确保场景类型为 UIWindowScene
        guard let windowScene = scene as? UIWindowScene else { return }
        
        // 2. 使用 windowScene 显式构造 UIWindow 实例（禁止使用无参 UIWindow()）
        let targetWindow = UIWindow(windowScene: windowScene)
        
        // 3. 构建根视图控制器并配置外观
        let mainViewController = MainTabViewController()
        targetWindow.rootViewController = mainViewController
        
        // 4. 持有并显示 window
        self.window = targetWindow
        targetWindow.makeKeyAndVisible()
        
        // 5. 处理冷启动传入的 URL 或 UserActivity（下文详解）
        handleInitialConnectionOptions(connectionOptions)
    }
    
    func sceneDidDisconnect(_ scene: UIScene) {
        // 场景从系统内存中断开时触发（并不意味着 App 进程终止）
        // 必须在此释放无法自动回收的强引用资源
    }
}
```

### 步骤 2：解耦 `AppDelegate` 里的 UI 初始化代码

将旧 `AppDelegate` 中创建 `self.window` 的代码完全移除，保持 `AppDelegate` 职责纯粹：

```swift
import UIKit

@main
final class AppDelegate: UIResponder, UIApplicationDelegate {

    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        // 仅保留全局 SDK 初始化、网络组件配置、推送 Token 注册等后台基础设施工作
        setupGlobalDependencies()
        return true
    }

    // MARK: - UISceneSession Lifecycle
    
    func application(
        _ application: UIApplication,
        configurationForConnecting connectingSceneSession: UISceneSession,
        options: UIScene.ConnectionOptions
    ) -> UISceneConfiguration {
        return UISceneConfiguration(
            name: "Default Configuration",
            sessionRole: connectingSceneSession.role
        )
    }
    
    private func setupGlobalDependencies() {
        // 示例：初始化日志库与底层组件
    }
}
```

### 步骤 3：统一深层跳转（DeepLink / Universal Link）拦截

在旧架构中，跳转逻辑写在 `application(_:open:options:)` 中。迁移到 Scene 架构后，跳转事件需要转移至 `SceneDelegate`，且**必须分为“冷启动”与“热启动”两种不同入口**：

```swift
final class SceneDelegate: UIResponder, UIWindowSceneDelegate {

    // 1. 热启动/后台唤醒：App 已在后台运行，用户点击 Scheme
    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        guard let targetURL = URLContexts.first?.url else { return }
        AppRouter.shared.routeTo(url: targetURL)
    }

    // 2. Universal Link 热启动处理
    func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
        if userActivity.activityType == NSUserActivityTypeBrowsingWeb,
           let webURL = userActivity.webpageURL {
            AppRouter.shared.routeTo(url: webURL)
        }
    }

    // 3. 冷启动处理：Scene 建立连接时，需主动检查 connectionOptions 里的上下文
    private func handleInitialConnectionOptions(_ options: UIScene.ConnectionOptions) {
        // 检查是否有 Scheme URL
        if let firstURLContext = options.urlContexts.first {
            AppRouter.shared.routeTo(url: firstURLContext.url)
            return
        }
        
        // 检查是否有 Universal Link / UserActivity
        if let userActivity = options.userActivities.first(where: { $0.activityType == NSUserActivityTypeBrowsingWeb }),
           let webURL = userActivity.webpageURL {
            AppRouter.shared.routeTo(url: webURL)
        }
    }
}
```

---

## 四、Flutter 开发者注意：Flutter App 的 Scene 架构强制迁移指南

许多 Flutter 开发者存在一个误区：认为 Flutter 应用有自己的 Widget 树和路由，不需要管 iOS 宿主的 Scene 架构。

**事实恰恰相反！** Flutter 应用运行在 iOS 宿主 Shell（即 `ios/Runner` 工程）之上。在传统 Flutter 项目模板中，`Runner/AppDelegate.swift` 继承自 `FlutterAppDelegate`，内部强关联了旧有的 `UIWindow`。当苹果强制推行 Scene 架构时，Flutter App 如果不完成宿主侧迁移，一旦使用 iOS 27 SDK 构建，将面临与原生 App 完全相同的后果——**启动即崩溃**；同时在 iPadOS 舞台调度、Slide Over 以及 macOS（Designed for iPad）等场景下，也会出现渲染冻结、黑屏或窗口尺寸错乱。

好消息是：**Flutter 官方已提供完整的 UIScene 生命周期支持**。该能力在 **Flutter 3.38** 中落地，并从 **Flutter 3.41** 起成为 iOS 工程的默认架构——符合条件的项目在升级后首次执行 `flutter run` 或 `flutter build ios` 时，Flutter 工具会**自动完成迁移**。因此对大多数 Flutter 开发者而言，最佳姿势不是手写 Scene 代码，而是先升级 Flutter SDK，再核对自动迁移的结果。

### 1. 官方迁移方案（推荐）

如果自动迁移未能覆盖你的工程（例如深度魔改过 `Runner`），可以按[官方迁移指南](https://docs.flutter.dev/release/breaking-changes/uiscenedelegate)手动迁移，共三步。

**第一步：在 `ios/Runner/Info.plist` 中声明 Scene 配置清单**

```xml
<key>UIApplicationSceneManifest</key>
<dict>
    <key>UIApplicationSupportsMultipleScenes</key>
    <false/>
    <key>UISceneConfigurations</key>
    <dict>
        <key>UIWindowSceneSessionRoleApplication</key>
        <array>
            <dict>
                <key>UISceneClassName</key>
                <string>UIWindowScene</string>
                <key>UISceneDelegateClassName</key>
                <string>$(PRODUCT_MODULE_NAME).SceneDelegate</string>
                <key>UISceneConfigurationName</key>
                <string>flutter</string>
                <!-- Flutter 官方模板保留 Main.storyboard，FlutterViewController 仍由 Storyboard 创建 -->
                <key>UISceneStoryboardFile</key>
                <string>Main</string>
            </dict>
        </array>
    </dict>
</dict>
```

**第二步：插件注册迁移至 `didInitializeImplicitFlutterEngine`**

采用 Scene 架构后，旧的 `application(_:didFinishLaunchingWithOptions:)` 不再是注册插件的安全时机。Flutter 提供了 `FlutterImplicitEngineDelegate` 协议，在隐式 FlutterEngine 初始化完成时回调：

```swift
import UIKit
import Flutter

@main
@objc class AppDelegate: FlutterAppDelegate, FlutterImplicitEngineDelegate {

    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }

    // 隐式 FlutterEngine 初始化完成时回调，在此注册插件
    func didInitializeImplicitFlutterEngine(_ engineBridge: FlutterImplicitEngineBridge) {
        GeneratedPluginRegistrant.register(with: engineBridge.pluginRegistry)
    }
}
```

**第三步（可选）：自定义 SceneDelegate 必须继承 `FlutterSceneDelegate`**

只有在需要自定义场景逻辑时才新建 `ios/Runner/SceneDelegate.swift`，且**必须**继承 Flutter 提供的 `FlutterSceneDelegate`：

```swift
import UIKit
import Flutter

final class SceneDelegate: FlutterSceneDelegate {
    // 按需覆写 scene(_:willConnectTo:options:) 等回调
    // 覆写时务必调用 super，保证事件继续转发给插件
}
```

> **⚠️ 为什么必须用 `FlutterSceneDelegate`**：它内部会把 `scene(_:openURLContexts:)`、`scene(_:continue:)` 以及前后台切换等场景事件**转发给 Flutter 插件**。如果像原生工程那样手写普通 `UIWindowSceneDelegate`，app_links / uni_links 深链、推送、统计等依赖生命周期事件的插件将**静默收不到任何回调**——这正是下文「踩坑 2」描述的那类线上 Bug 在 Flutter 侧的翻版。若因架构原因确实无法继承它，可以改为遵循 `FlutterSceneLifeCycleProvider` 协议，借助 `FlutterPluginSceneLifeCycleDelegate` 手动完成事件转发。

### 2. 迁移后的行为变化（回归验证清单）

采用 Scene 架构后，以下旧行为会发生变化，建议列入迁移后的回归清单：

* `UIApplication.shared.delegate?.window` 变为 `nil`——宿主侧依赖它取窗口的代码需要改造（参考下文「踩坑 1」）。
* UIKit **不再调用** `AppDelegate` 中的 `applicationDidBecomeActive(_:)`、`applicationWillResignActive(_:)` 等 UI 生命周期方法。
* `application(_:didFinishLaunchingWithOptions:)` 的 `launchOptions` 恒为 `nil`，冷启动上下文需改从 Scene 的 `connectionOptions` 获取。

### 3. 临时退出方案（过渡窗口期）

如果迁移引发暂时无法解决的兼容问题，Flutter 提供了两个临时退路，为团队争取过渡时间：

* 在 `Info.plist` 中将 `UIApplicationSceneManifest` 的 key 加上下划线前缀（`_UIApplicationSceneManifest`），可临时停用 Scene 架构；
* 在 `pubspec.yaml` 中关闭自动迁移提示：

```yaml
flutter:
  config:
    enable-uiscene-migration: false
```

> **⚠️ 注意**：临时方案只在 iOS 27 强制生效前有效，务必在 iOS 27 SDK 成为团队构建基线之前完成正式迁移。

### 4. 进阶：手动管理 FlutterEngine 的场景

只有以下两类场景才需要手动创建 `FlutterEngine` 与 `FlutterViewController`：

* **add-to-app 混合工程**：Flutter 页面作为原生宿主 App 的一部分嵌入，需要共享或复用 Engine；
* **iPadOS 多窗口**（`UIApplicationSupportsMultipleScenes = true`）：单个 `FlutterEngine` 无法驱动两个并发页面，此时应使用 Flutter 官方推荐的 `FlutterEngineGroup`，在每个 Scene 连接时通过 `engineGroup.makeEngine()` 派生新引擎，既省内存又能完美支持多 Scene 并发渲染。

手动管理 Engine 时同样要牢记：插件事件转发依赖 `FlutterSceneDelegate` 体系，自定义 SceneDelegate 务必按上文说明接入事件转发。

> **💡 老版本 Flutter 的取舍**：如果项目锁定在 Flutter 3.38 之前，官方 Scene 支持尚不存在，手写桥接的兼容成本很高（插件生命周期事件全部需要自行转发）。对这类项目而言，最务实的选择仍然是升级 Flutter SDK 后按官方路径迁移，而不是长期维护一套自制桥接层。

---

## 五、生产环境踩坑防护与最佳实践

### 踩坑 1：废弃 `keyWindow` 后的安全获取方案

在旧代码中，经常可以看到类似 `UIApplication.shared.keyWindow?.rootViewController` 的写法。在 iOS 13+ 中，`keyWindow` 已经被官方标记为废弃（Deprecated）。在多 Scene 场景下，全局可能同时存在多个 `keyWindow`。

**正确姿势**：封装一个全局 Safe Utility 类，通过遍历寻找当前前台活跃的 `UIWindowScene`：

```swift
enum WindowSceneProvider {
    
    /// 获取当前前台活跃的 UIWindowScene
    static var activeWindowScene: UIWindowScene? {
        return UIApplication.shared.connectedScenes
            .compactMap { $0 as? UIWindowScene }
            .first { $0.activationState == .foregroundActive }
    }
    
    /// 获取当前前台活跃 Scene 的 Key Window
    static var activeKeyWindow: UIWindow? {
        return activeWindowScene?.windows
            .first { $0.isKeyWindow }
    }
}
```

### 踩坑 2：冷启动推送/跳转漏掉 `connectionOptions` 的线上 Bug

这是绝大多数团队在刚切换至 `SceneDelegate` 时最容易出现的漏洞：只写了 `scene(_:openURLContexts:)`，却在 `scene(_:willConnectTo:options:)` 中**忘记了解析 `connectionOptions`**。

导致的结果是：如果 App 已经在后台运行，点击 Scheme 能正常跳转；但如果 App 被杀掉了进程，点击 Scheme 冷启动 App 时，只能进入首页，无法正确跳转到目标落地页。

**防坑黄金法则**：在 `scene(_:willConnectTo:options:)` 完成 `window.makeKeyAndVisible()` 之后，**务必显式调用一次链接与上下文解析函数**。推送点击的冷启动同理——需检查 `connectionOptions.notificationResponse`，否则用户从通知栏冷启动 App 时同样会丢失目标落地页。

### 踩坑 3：单例持有 `UIWindow` 导致内存泄漏与视图错乱

在多 Scene 或 iPadOS/visionOS 场景中，如果某个全局单例组件（如 Toast / Loading HUD / 自定义 Alert）私有持有了某个 `UIWindow` 实例，当系统销毁该 Scene（触发 `sceneDidDisconnect`）时，该 Window 及其挂载的所有视图都会因为强引用而无法释放，造成严重的内存泄漏与视图渲染错乱。

**最佳实践**：
* 避免在单例中长期存储 `UIWindow` 实例。
* 全局弹窗组件应优先通过当前活跃 Scene 的 `topViewController` 呈现，或者动态从 `WindowSceneProvider.activeWindowScene` 创建和解绑临时 Window。

---

## 写在最后

从传统的 `AppDelegate` 转型至 `UISceneDelegate`，表面上只是增加了几行配置和模板代码，但其背后代表的是苹果对系统 UI 架构的现代化重构思维：**剥离进程管理与界面渲染，用抽象的“场景（Scene）”来承载多终端、多形态的展示形式**。

无论是原生 iOS 还是 Flutter 跨平台项目，迎合苹果官方的硬性合规要求、完成 Scene 架构的升级，不仅能帮我们彻底厘清复杂的 App 冷/热启动跳转逻辑，更能让项目轻松应对 iPadOS 多窗口、分屏协作以及未来新形态系统的扩展要求。如果你的项目还在依赖旧有的单 Window 结构，不妨从今天起，按照本文的指南完成一次优雅的架构焕新。

---

*本文首发于微信公众号「iOS观之」（微信号：run88184），欢迎关注。*
