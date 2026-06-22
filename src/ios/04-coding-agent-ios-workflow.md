---
title: AI 时代，iOS / Flutter 开发者该怎么用好 Coding Agent？
cover: ../assets/cover-coding-agent-ios.png
---

# AI 时代，iOS / Flutter 开发者该怎么用好 Coding Agent？

> Coding Agent 不是一个「替你写 App 的外包」，更像一个速度很快、但需要明确指挥和严格验收的初级队友。对同时做 iOS 原生和 Flutter 的开发者来说，真正要学的不是把代码都交出去，而是知道什么该交、怎么交、怎么验收。

---

## 前言

讨论 AI 对 iOS / Flutter 开发的影响时，一个基本判断是：AI 确实吃掉了一部分样板代码和重复劳动，但还吃不掉平台理解、跨端架构判断、体验审美和线上质量。

这篇文章想继续往前走一步：如果 Coding Agent 已经进入日常开发，那 iOS / Flutter 开发者到底该怎么用？

现在很多人用 AI 写代码，还是一种很粗糙的方式：

> 帮我做一个登录页。
>
> 帮我接一下这个接口。
>
> 帮我修一下这个 bug。

然后 AI 生成一大段代码，看起来很完整，复制进去也许还能跑。但真实项目不是 demo。它可能同时有 Swift / Objective-C、Dart、Flutter Module、原生插件、MethodChannel、证书签名、系统版本、真机体验、App Store 规则，还有一堆历史代码。

所以问题不是「要不要用 AI」，而是：**怎么把 Coding Agent 放进一个可控的工程流程里。**

---

## 一、先分清：Coding Agent 适合做什么

Coding Agent 最适合做的，不是替你拍板，而是替你省掉那些明确、重复、边界清楚的工作。

### 1. 写样板代码

SwiftUI 或 Flutter 里的列表、表单、设置页、空状态、加载状态，这些 UI 结构本身很模式化。只要你把输入、输出和交互边界讲清楚，AI 通常能给出一个不错的起点。

比如：

- Model / DTO / Repository 基础结构
- URLSession / Alamofire 请求封装
- SwiftUI Preview mock 数据
- Flutter Widget、StateNotifier / Controller、mock 数据
- 协议实现和默认实现
- 简单的错误展示和 loading 状态

这些代码不一定能直接进主分支，但它能帮你把第一版结构搭出来。

### 2. 做局部重构

Coding Agent 很适合处理小范围、目标明确的重构。

比如把一个过长的 SwiftUI View 拆成几个子 View，把 Flutter 里的大 Widget 拆成小组件，把 callback 改成 async/await，把重复的 formatter 提取成 helper，把命名混乱的变量统一掉。

这类工作有一个特点：你知道目标是什么，也知道验收标准是什么。AI 只是帮你更快完成机械修改。

### 3. 补测试和边界用例

很多项目不是不需要测试，而是大家没时间写测试。AI 在这件事上很有价值。

尤其是 ViewModel、Controller、Repository、纯函数、状态流转这类代码，只要你给出输入输出，AI 可以帮你快速补上：

- 成功路径
- 失败路径
- 空数据
- 重复点击
- loading 状态
- mock repository

测试不应该全部靠 AI 判断，但 AI 可以显著降低「开始写测试」的阻力。

### 4. 辅助 Debug

遇到 crash log、控制台报错、构建失败、SwiftUI 奇怪警告、Flutter 红屏、Dart analyze 报错时，把日志交给 AI 分析是有价值的。

但这里要注意：AI 给出的不是结论，而是排查方向。

它可以帮你列出可能原因、解释错误含义、提示相关 API 限制，但真正的验证还是要靠你自己：做最小复现、加日志、跑真机、看 Instruments。

### 5. 写文档和迁移说明

很多项目缺文档，不是因为文档不重要，而是因为写文档太容易被排到最后。

Coding Agent 可以帮你：

- 总结模块职责
- 生成 README
- 整理接口说明
- 解释复杂类的状态流
- 写重构前后的迁移说明

这些文字工作不一定有技术含量，但能明显提高团队协作效率。

---

## 二、也要清楚：哪些事情不能直接甩给 Coding Agent

AI 写得快，不代表它能替你负责。

下面这些事情，不能直接一句话甩给 Coding Agent。

### 1. 架构决策

一个模块到底用 MVVM、TCA，还是简单的 View + ViewModel 就够了；一个 Flutter 页面到底用 Riverpod、Bloc，还是普通 Controller 就够了，这不是 AI 能脱离上下文判断的。

AI 很容易为了「看起来完整」引入过度设计：多一层 manager、多一个 coordinator、多一套状态同步、多几个 protocol。代码看起来很工程化，但项目复杂度也被悄悄抬高了。

架构决策必须由人来做。AI 可以给备选方案，但不能替你拍板。

### 2. 支付、订阅、登录、安全相关逻辑

StoreKit、收据验证、登录态、Token 刷新、Keychain、权限控制，以及 Flutter 和原生之间传递敏感数据的桥接逻辑，这些地方不能靠「看起来对」。

它们的 bug 不只是崩溃，还可能影响收入、用户数据和审核风险。AI 可以帮你查 API、写测试、解释流程，但核心逻辑必须人工审查。

尤其是内购和订阅，沙盒环境、线上环境、恢复购买、跨设备同步、退款和过期状态都要单独验证。

### 3. 复杂导航和 Deep Link

iOS / Flutter 混合 App 的导航复杂度经常被低估。

一个看似简单的「跳转到订单详情」，可能来自首页点击、推送点击、Universal Link、Widget、冷启动恢复、登录后重定向。目标页面可能在原生侧，也可能在 Flutter 路由里。每个入口的状态都不同。

AI 很容易只跑通「从首页点进去」这一条路径，然后漏掉冷启动、登录拦截、Tab 切换、Flutter engine 初始化和多层 sheet。

### 4. 证书、签名、构建配置

证书、Provisioning Profile、Capability、Bundle ID、APNs Key、Team 配置，以及 Flutter iOS 产物里的 Pod、Generated.xcconfig、Runner 配置，这些问题高度依赖本地环境和 Apple Developer 后台状态。

AI 可以帮你列排查清单，但不能替你看到 Xcode 里的真实配置，也不能替你判断开发者账号里的证书关系。

这类问题最怕盲目执行。AI 给十个方案，你一个个乱试，项目配置可能更乱。

### 5. 体验判断

动画是不是太慢，Haptic 是按下触发还是成功后触发，键盘弹出时输入框是不是被挡住，权限弹窗是不是出现得太早，Flutter 页面和原生页面切换有没有割裂感，这些都不是编译器能告诉你的。

AI 可以生成一版交互，但体验必须上真机看。

iOS 用户对手感很敏感。很多时候，差距不在代码有没有写，而在原生和 Flutter 的体验细节有没有被认真调过。

---

## 三、正确工作流：把大任务拆成可验收的小任务

用 Coding Agent 最大的坑，是把一个模糊大任务直接丢给它。

### 1. 不要说「帮我做一个登录页」

坏例子：

```
帮我写一个登录页。
```

这句话太空了。AI 不知道你的项目结构，不知道设计风格，不知道状态从哪里来，也不知道点击事件应该怎么交给 ViewModel 或 Flutter Controller。

更好的写法是：

```
在现有 SwiftUI 项目中新增 LoginView。

要求：
1. 只负责 UI，不调用 API。
2. 包含手机号输入、验证码输入、获取验证码按钮、登录按钮。
3. 登录按钮状态由外部传入的 isLoading 控制。
4. 点击事件通过 closure 暴露给 ViewModel。
5. 样式尽量复用项目里已有的字体、颜色和 ButtonStyle。
6. 不要修改其他文件。
```

这才是一个可执行、可检查、可回滚的任务。

如果是 Flutter，也应该写到同样具体：

```
在现有 Flutter 项目中新增 LoginPage。

要求：
1. 只负责 UI，不直接调用 API。
2. 使用项目现有的 Controller / ViewModel 管理状态。
3. 包含手机号输入、验证码输入、获取验证码按钮、登录按钮。
4. loading、errorMessage、canSubmit 由外部状态控制。
5. 点击事件通过 controller 方法触发。
6. 所有 JSON 解析遵守项目现有规范。
7. 不修改路由表和网络层。
```

### 2. 先让 Agent 读上下文，再让它动手

在真实项目里，不要一上来就让 Agent 写代码。

先让它阅读和总结现有上下文：

- 当前页面的相似实现
- 网络层调用方式
- ViewModel 状态管理方式
- Flutter 页面状态管理方式
- 路由和 Deep Link 入口
- MethodChannel / EventChannel 封装方式
- 项目已有代码规范

比如你要新增一个订单列表页，不要直接说「写一个 OrderListView」或「写一个 OrderListPage」。更稳的做法是先让它看已有的用户列表页、商品列表页、订单详情页，让它总结项目里列表页的组织方式，再基于这个模式生成新页面。

Agent 不是越自由越好。上下文越清楚，它越不容易发明一套和项目风格不一致的新写法。

如果项目比较大，不要让 Agent 每次都全量扫描。可以单独维护 `AGENTS.md`、`docs/project-map.md`、`docs/component-map.md` 这类项目索引，让它先读索引，再读取和当前任务直接相关的文件。这个话题更适合单独展开。

### 3. 先让 AI 出方案，不急着写代码

对于稍微复杂一点的改动，不要一上来就让 AI 改文件。

先让它回答三个问题：

- 准备改哪些文件？
- 每个文件改什么？
- 为什么这么改？

如果方案里出现了不必要的新抽象、跨层调用、全局状态修改，你可以在写代码之前把方向纠正回来。

很多问题不是代码写错，而是第一步方向就错了。

### 4. 一次只让它改一个小范围

Coding Agent 的上下文越大，越容易顺手扩大修改范围。

比较稳的粒度是：

- 一个 SwiftUI View
- 一个 Flutter Widget
- 一个 ViewModel
- 一个 Controller
- 一个 Repository 方法
- 一个测试文件
- 一个明确 bug 修复点

不要让它同时改 UI、接口、路由、缓存和登录态。人类 code review 也受不了这种 diff。

### 5. 每一步都要跑验证

AI 写完代码之后，至少要做这几件事：

- 编译
- 跑单测
- `dart analyze`
- `flutter test`
- 看关键页面
- 真机验证交互
- 检查 diff 是否越界

如果是登录、支付、订阅、推送、Deep Link、Flutter / 原生跳转，还要单独做路径回归。

「能编译」只是最低门槛，不是完成标准。

---

## 四、iOS / Flutter 项目里的 Prompt 模板

下面这些模板，不是为了追求一句话魔法，而是为了把任务边界讲清楚。这个思路和 Codex 官方最佳实践里强调的「给足上下文、复杂任务先计划」是一致的；放到 iOS / Flutter 项目里，就是把页面职责、状态来源、测试方式、跨端边界写清楚。

### 1. SwiftUI 页面 Prompt

```
请在现有 SwiftUI 项目中实现一个 OrderListView。

要求：
1. 只写 UI，不直接调用 API。
2. 数据由外部传入：[OrderItemViewData]。
3. 空列表时展示空状态。
4. loading 状态由外部传入 isLoading 控制。
5. 点击订单时通过 onTapOrder(OrderItemViewData) 回调给外部。
6. 不新增全局样式，不修改其他业务文件。
7. 生成必要的 Preview mock 数据。
```

这个 Prompt 的核心是：让 View 保持 View，不让它偷偷承担业务层职责。

### 2. ViewModel Prompt

```
请为 OrderListView 实现 OrderListViewModel。

要求：
1. 使用 @MainActor。
2. 状态包含 idle、loading、success、failure。
3. 通过 OrderRepository 注入数据来源。
4. loadOrders() 负责加载订单列表。
5. 错误统一转换成页面可展示的 message。
6. 不在 ViewModel 中写网络请求细节。
7. 补充基础单元测试。
```

这里的重点是状态和依赖边界。ViewModel 可以组织业务状态，但不要直接越过 Repository 调 API。

### 3. Repository Prompt

```
请实现 OrderRepository 的 fetchOrders(userId:) 方法。

要求：
1. 使用现有 ApiClient。
2. 不处理 UI 状态。
3. 将接口 DTO 转换成领域层 OrderModel。
4. 保留现有错误处理方式。
5. 不修改 ApiClient 的公共行为。
6. 为 DTO 转换补充测试。
```

Repository 的边界一定要讲清楚。否则 AI 很容易把 loading、toast、页面跳转都塞进来。

### 4. Flutter 页面 Prompt

```
请在现有 Flutter 项目中实现 OrderListPage。

要求：
1. 只写页面 UI 和必要的状态绑定，不直接调用 API。
2. 列表必须使用 ListView.builder。
3. 数据由 OrderListController / ViewModel 提供。
4. 页面包含 loading、empty、error、content 四种状态。
5. TextStyle 必须显式设置 color。
6. 点击订单时调用 controller.openOrderDetail(orderId)。
7. JSON 解析不要手写 fromJson，遵守项目里的 g_json 规范。
8. 不修改路由表、网络层和全局主题。
```

Flutter 的 Prompt 要把项目规范说清楚，尤其是列表懒加载、样式、JSON 解析和状态归属。否则 AI 很容易写出能跑但不符合团队规范的页面。

### 5. Flutter / 原生桥接 Prompt

```
请为 Flutter Module 新增一个获取 iOS 设备能力的 MethodChannel 调用。

要求：
1. Dart 侧只定义平台接口和返回模型。
2. iOS 侧用 Swift 实现 MethodChannel handler。
3. channel name 使用项目已有命名风格。
4. 所有返回字段必须有明确类型，不返回动态 Map 给业务层直接使用。
5. iOS 侧错误使用 FlutterError 返回。
6. Dart 侧把平台异常转换成业务层可识别的 failure。
7. 不在桥接层处理 UI 展示。
8. 补充 Dart 侧单元测试或 mock 示例。
```

混合开发里，桥接层是最容易被 AI 写乱的地方。一定要强调类型、错误处理和职责边界，不要让 MethodChannel 变成一个随手塞业务逻辑的万能入口。

### 6. Debug Prompt

```
下面是 iOS crash log / Flutter 控制台日志 / Dart analyze 输出。

请你：
1. 先判断最可能的 3 个原因。
2. 每个原因给出验证方法。
3. 不要直接改代码，先给排查步骤。
4. 标记哪些结论只是推测。
5. 如果需要更多信息，请列出应该补充的日志或断点位置。
```

Debug Prompt 最重要的一点是：不要让 AI 直接进入「修复模式」。先让它给排查路径。

### 7. Code Review Prompt

```
请以 iOS / Flutter code review 的方式审查下面 diff。

重点关注：
1. 生命周期问题
2. retain cycle
3. 主线程 / MainActor / Flutter setState 时机
4. 错误处理
5. 状态一致性
6. 是否破坏现有架构
7. 是否扩大了修改范围
8. Flutter Widget 是否过大、是否缺少懒加载
9. MethodChannel 是否类型清晰、错误处理完整

只列出明确问题和风险，不要泛泛建议。
```

AI 做 code review 的价值，不是替代人，而是帮你做第一轮扫描。它可以提醒你一些低级风险，但最终判断仍然要靠人。

---

## 五、用 Coding Agent 时，iOS / Flutter 开发者要守住的几条底线

工具越强，越需要边界。

### 1. 不接受看不懂的代码

不管代码是谁写的，只要你看不懂，就不应该合进去。

AI 生成的代码尤其容易出现一种情况：结构看起来很完整，命名也很专业，但里面的状态流和边界处理经不起推敲。

看不懂，就让它解释；解释完还不清楚，就让它重写得更简单。

### 2. 不让 AI 偷偷扩大修改范围

原本只让它改一个 View，结果它顺手改了路由、改了 API、改了全局状态，这是危险信号。

真实项目里，修改范围越大，回归成本越高。Coding Agent 写代码很快，但你 review 和验证的成本不会凭空消失。

### 3. 不用「能跑」代替「正确」

一个功能能跑起来，不代表它是正确的。

它可能没有处理失败状态，没有处理重复点击，没有处理网络超时，没有处理登录过期，没有处理页面销毁后的回调，也可能没有处理 Flutter 页面 dispose 之后的异步状态更新。

iOS / Flutter 开发里很多 bug 都不是第一眼能看到的。越是 AI 生成的代码，越要看边界。

### 4. 不把测试交给运气

如果 AI 改了 ViewModel 或 Controller，就让它补对应的状态测试。

如果 AI 改了 Repository，就让它补 DTO 转换和错误分支测试。

如果 AI 改了 Deep Link，就列出冷启动、登录态、Tab 切换、目标页面不存在、Flutter engine 未初始化这些路径。

测试不是为了证明 AI 写得好，而是为了证明这段代码能承担真实项目的复杂度。

### 5. 不让项目变成 prompt 堆出来的迷宫

最危险的不是 AI 写错一段代码，而是它在每个需求里都临时补一点逻辑。

今天加一个 manager，明天加一个 helper，后天加一个 state cache。每一段都能解释，但合在一起就变成没人敢动的迷宫。

AI 可以写局部实现，但项目的结构边界必须由人维护。

### 6. 不让跨端边界变模糊

iOS + Flutter 项目里，最怕的是边界慢慢糊掉。

今天让 Flutter 直接关心原生登录态，明天让原生直接拼 Flutter 业务参数，后天 MethodChannel 里开始处理 UI 跳转。每一步看起来都只是「方便一下」，但最后会变成两边都不敢改。

用 Coding Agent 时要把边界写清楚：哪些逻辑属于 Flutter，哪些属于 iOS 原生，哪些只允许放在桥接层。AI 可以帮你写桥，但不能让桥变成业务垃圾桶。

### 7. 不把敏感信息交给 AI

不要直接粘贴真实 token、证书、私钥、生产环境配置、用户手机号、订单数据和完整线上日志。

如果必须让 AI 分析日志，先做脱敏：替换用户标识、隐藏请求头、裁掉无关字段，只保留定位问题需要的信息。

Coding Agent 是开发工具，不应该变成敏感信息的出口。

---

## 六、未来的 iOS / Flutter 开发者，更像技术负责人

过去，很多开发者的能力重心是：我能不能把代码写出来。

AI 之后，能力重心会慢慢变成：

- 我能不能把目标拆清楚
- 我能不能给出明确约束
- 我能不能审查 AI 的输出
- 我能不能设计验证路径
- 我能不能守住原生和 Flutter 的架构边界
- 我能不能保证跨端体验质量

Coding Agent 会降低写代码的成本，但会放大判断、审查、验证能力的价值。

真正强的 iOS / Flutter 开发者，不是不用 AI，而是用 AI 之后，项目依然干净、稳定、可维护。

随着 AI 能力继续增强，我们的工作方式还会再变一次。

第一阶段，是让 AI 写代码：补页面、补测试、改小 bug。

第二阶段，是让 AI 做任务：它可以自己读代码、拟方案、改文件、跑测试、修失败，再把结果交给你 review。

第三阶段，开发者要做的会更像「定义工程系统」：把架构规则写进项目文档，把代码规范固化到 lint 和 CI，把关键路径变成自动化测试，把发布前检查做成 checklist。这样 AI 越强，项目越受益；而不是 AI 越能写，项目越失控。

所以后面真正要做的，不是把每个 prompt 写得越来越长，而是把团队的工程判断沉淀成规则、测试和流程。让 AI 在这些边界里加速，而不是在边界外自由发挥。

---

## 参考资料与延伸阅读

这篇文章里的方法不是凭空总结，下面这些官方资料值得配合看：

- Apple Developer：[Xcode 27 Coding Intelligence](https://developer.apple.com/xcode/whats-new/)  
  Apple 对 Xcode 27 Coding Agents 的官方介绍，适合了解 Xcode 里 agentic coding 的定位。

- Apple Developer：[Writing code with intelligence in Xcode](https://developer.apple.com/documentation/Xcode/writing-code-with-intelligence-in-xcode)  
  官方文档里明确提到可以用 agent / model 生成代码、理解陌生代码库、修 bug 和重构。

- OpenAI Developers：[Codex best practices](https://developers.openai.com/codex/learn/best-practices)  
  重点看「Context and prompts」「Plan first」几部分，和本文的工作流最相关。

- OpenAI Developers：[Codex prompting](https://developers.openai.com/codex/prompting)  
  说明为什么要给 agent 提供相关文件、上下文和明确任务边界。

- Flutter Docs：[Platform channels](https://docs.flutter.dev/platform-integration/platform-channels)  
  Flutter 官方关于 MethodChannel / 平台通信的说明，是处理 Flutter 与 iOS 原生桥接的基础资料。

- Flutter Docs：[Testing Flutter apps](https://docs.flutter.dev/testing/overview)  
  Flutter 官方测试总览，适合配合本文里的 `flutter test`、widget test、integration test 思路一起看。

---

## 写在最后

Coding Agent 最适合替你省掉重复劳动，不适合替你承担工程判断。

iOS / Flutter 开发者要做的，不是和 AI 比谁敲代码快，而是学会把 AI 放到正确的位置：让它写样板、补测试、查资料、做局部重构；自己守住架构、跨端边界、体验、验证和上线质量。

AI 时代，写代码的人不会消失，但只会写代码的人会越来越被动。

真正稀缺的是：能把一个想法稳定落到 Apple 平台上，并在原生与 Flutter 之间保持清晰边界的工程判断力。

---

*本文首发于微信公众号「iOS观之」（微信号：run88184），欢迎关注。*
