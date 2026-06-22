---
title: WWDC26：iOS 开发者需要关注的新变化
cover: ../assets/cover-wwdc26-highlights.jpeg
---

# WWDC26：iOS 开发者需要关注的新变化

> 今年的 WWDC，Apple 把 AI 从「锦上添花」变成了「系统基础设施」。本文盘点 iOS 开发者真正需要关注的变化，不做通稿式罗列。

---

## 前言

WWDC26 于 2026 年 6 月 8 日至 12 日举行。iOS 27、Xcode 27、macOS 27……所有系统都迎来了年度大版本更新。但和往年不同，今年的主题不再是某个 Widget 改版、某个控件增强，而是一个贯穿所有更新的关键词：**AI 落地**。

作为一个每天和 Xcode 打交道的一线开发者，我从上百场 Session 中梳理出了真正值得关注的部分：一套大幅扩展的 AI 调用入口、一个全新的设备端模型框架、一个升级后的意图系统，以及一条 AI 加持的开发工具链。下面逐一来看。

---

## 一、AI 全面落地：一个扩展，一个新增

这届 WWDC 最核心的开发者变化，是 AI 能力从「系统自带功能」进一步开放到开发者手里。这里最值得看的是两条线：**Foundation Models Framework 的大幅扩展**，以及 **Core AI 这个全新设备端模型框架**。

### 1. Foundation Models Framework：一套协议，统一 AI 入口

**Foundation Models Framework** 是一套原生 Swift API，用于调用 Apple 自研的 Foundation Models——也就是驱动 Apple Intelligence 的那套底层模型。

今年它的重点不是「从无到有」，而是能力边界被明显扩宽。新的 **Language Model 协议** 让你可以用同一套 API 对接不同模型来源：

| 模型来源 | 说明 |
|---|---|
| Apple Foundation Models | 设备端自研模型，驱动 Apple Intelligence 的核心引擎 |
| 云端模型（Claude、Gemini 等） | 通过同一套协议接入，无需为每个供应商学一套 API |
| 自定义 Provider | 只要遵循协议，任何模型都能挂进来 |

这套设计的巧妙之处在于——**Apple 没有把开发者锁死在自家模型里**。它承认了多模型生态的现实，然后用一套 Swift 协议把选择权交给了你。

**值得关注的特性：**

- **多模态 Prompt**：同时传入图片和文字，模型可以关联理解。Vision 框架的工具（OCR、条形码读取）也能在设备端被模型直接调用。
- **动态 Profile**：在同一个持续会话中，可以实时切换模型、工具和指令。比如用户在聊天过程中从「翻译模式」切到「摘要模式」，不需要重启上下文。
- **Private Cloud Compute 免费额度**：参加 App Store Small Business Program（累计下载量 < 200 万）的 App，可以免费使用 Apple 的云端推理服务。
- **Evaluations 框架**：专门的 AI 行为验证工具。不再靠手工跑几个 case 来「感觉没坏」，而是动态覆盖各种条件，回归测试级别的可靠。
- **fm CLI + Python SDK**：非 Xcode 场景也能玩——在命令行和 Python 脚本里直接跑 AI 推理。

> 一句话：Foundation Models 正在把「在自己的 App 里集成 AI 能力」这件事，从零散调用第三方 SDK，变成更接近系统层级的原生开发体验。

### 2. Core AI：把模型跑在设备端，省掉服务端和 Token 成本

如果 Foundation Models 解决的是「如何调用模型」的问题，那么 **Core AI** 解决的是「如何把模型跑在设备上」的问题。

这是一套操作系统级别的框架，**专为 Apple Silicon 设计**：

| 特性 | 含义 |
|---|---|
| 零服务端依赖 | 不需要为了推理单独架服务器、调云端 API |
| 零 Token 成本 | 设备端推理不按云端 Token 计费 |
| 自带模型 | 可以把自己的模型打包进 App，在设备上直接跑 |
| Swift 原生 API | 现代化、内存安全的 Swift 接口，用于加载、特化、运行 AI 模型 |
| AOT 编译 | 模型提前编译为机器码，加载速度大幅提升 |
| 细粒度内存控制 | 零拷贝数据路径、有状态执行，对推理性能的精细把控 |
| Metal Tensor | 自定义 ML 算子可以用 Metal 优化 |
| 全平台覆盖 | 从小型视觉模型到大规模生成式 AI，iOS/macOS/tvOS/visionOS 全支持 |

> Core AI 和 Foundation Models 的关系：前者偏向「把自己的模型部署到设备端」，后者偏向「统一调用 Apple 模型、云端模型或自定义 Provider」。两者互补，共同构成了 Apple 在 AI 时代的基础设施层。

---

## 二、App Intents 大升级：Siri 终于懂你的 App 了

从 iOS 16 引入 App Intents 开始，Apple 就一直在推动开发者把 App 能力接入 Siri、Shortcuts、Spotlight 等系统入口。前几年一直有推进，但更多是在补齐可用性。今年的更新，可以说是 App Intents 发布以来最大的一次升级。

### 核心变化：从「硬编码短语」到「自然语言理解」

过去你做 App Intents，需要预先定义一组相对明确的短语（"Send money to XXX"、"Check balance"），Siri 主要依赖这些短语来触发能力。现在变了：

| 新特性 | 说明 |
|---|---|
| **Entity Schemas** | 将 App 内的内容实体（订单、商品、联系人等）贡献给 Spotlight 语义索引。Siri 可以**主动**向用户推荐这些内容，并带着 App 的归因链接 |
| **Intent Schemas** | 用户用自然语言描述意图，无需硬编码触发短语。Siri 的语义理解能力升级，开发者不需要随着 Siri 的每次更新改代码 |
| **View Annotations API** | 把你屏幕上的视图映射为实体。用户在 App 内可以说「把这个发给他」「保存第一张图」——Siri 知道屏幕上有什么，也知道你在指哪个 |

### 测试框架也来了

App Intents 新增了 **App Intents Testing framework**，可以验证整套集成是否正常——不需要写 UI 自动化脚本，直接在系统级通道里跑，比端到端测试更底层也更可靠。

> 如果你的 App 还没接入 App Intents，今年是最好的时机。Apple 在 Siri 上投入的 AI 能力，最终需要开发者用 App Intents 来接入。

---

## 三、Xcode 27：Agent 时代的开发工具

每年 Xcode 都会有改进，但 Xcode 27 的步子迈得比往年大得多。

### Coding Agents：AI 不再是补全，而是协作者

Xcode 27 最重要的变化是 **Coding Agents**——嵌入 IDE 的 AI 智能体。和代码补全不同，Agent 能理解多步骤任务：

- **覆盖全流程**：从原型搭建、功能实现到代码打磨，Agent 伴随整个开发周期
- **后台运行**：机械性工作（生成样板代码、批量重命名、写测试）可以丢给 Agent，你不用盯着等
- **多模型选择**：可以根据任务选择不同的底层模型，不绑定单一供应商
- **单人/团队通用**：工作流一致，不因为协作方式不同而改变使用体验

### 本地化也能丢给 Agent

Xcode 27 的 Agent 可以直接处理本地化链路：

- 添加新语言
- 更新 String Catalog
- 翻译字符串
- 审查和迭代翻译结果
- 根据 App 上下文添加复数变体

Xcode 会自动为 Agent 提供项目的上下文和语言特定的风格指南，确保翻译质量不跳脱 App 的调性。

### Device Hub：真机 + 模拟器统一管理

新增 **Device Hub** 面板，把设备和模拟器放在同一个视图里管理：

- 不需要切出 Xcode 就能诊断和复现问题
- 检查设备状态
- 简化测试流程

以前偶尔要用 Xcode 跑，偶尔要切到 Simulator.app 调，现在统一了。

### Instruments 大幅增强

性能调试工具也迎来了一轮重要更新：

| 增强 | 说明 |
|---|---|
| Swift Concurrency 改进 | 异步任务调度、Actor 竞争、线程使用情况可视化 |
| Top Functions 增强 | 快速定位 Trace 中最重的调用栈 |
| Run Comparison | 修改前后对比，验证优化效果，修复有据可依 |
| 整体流程优化 | Profile → 定位 → 修复 → 验证，每一步耗时都缩短了 |

> Swift Concurrency 的加强尤其值得关注。随着 Swift 6 强制严格并发检查，越来越多的项目开始迁移。Instruments 现在能清晰展示 actor 之间的竞争、任务在哪里被挂起——这些过去几乎是盲区。

---

## 四、SwiftUI & UIKit & WidgetKit

每年代际更新的 UI 框架变化，今年也不少。

### SwiftUI

| 新特性 | 说明 |
|---|---|
| 文档类 App 直读磁盘 | 高性能文件访问，适合笔记、编辑器、办公类应用 |
| 列表/网格拖拽排序 | 用户自由拖拽重排内容，跨列表和网格 |
| Lazy 预加载 | 懒加载子视图时自动预取内容，滚动更丝滑 |
| 图形特效合成 | 多层效果叠加，比旧版更灵活 |
| 视觉刷新 | 新材质（materials）、优化排版、Tab Bar 和导航栏样式更新 |

### UIKit

UIKit 没被遗忘——新增了专门适配 **iPhone Mirroring** 的布局能力，让 App 在 Mac 上镜像使用时体验更好。这是实用导向的增强，不炫但好用。

### WidgetKit

Widget 现在可以通过 **App Intents 定制化**，用户能自己调整小组件的展示内容和样式。结合动态样式支持，同一个 Widget 可以呈现更丰富的形态。

---

## 五、普通 iOS 项目应该先看什么？

WWDC 的信息量很大，但普通项目不需要一上来就全部接入。更现实的顺序是：先判断它和你当前业务的距离。

| 项目类型 | 优先关注 |
|---|---|
| 工具类、内容类 App | Foundation Models、App Intents |
| 电商、订单、CRM 类 App | Entity Schemas、Intent Schemas、Spotlight 语义索引 |
| 音视频 App | NowPlaying、Music Understanding |
| 文档、编辑器、生产力 App | SwiftUI 文档能力、拖拽排序、Foundation Models |
| 正在迁移 Swift 6 的项目 | Xcode 27、Instruments、Swift Concurrency 调试能力 |
| 暂时没有明确 AI 场景的 App | 先梳理 App Intents 的实体和动作，不必为了追热点硬接 AI |

我的建议是：**先建模，再接 AI**。

很多 App 现在最大的问题不是缺少大模型，而是自己的业务能力没有被系统理解。订单是什么、用户能对订单做什么、当前屏幕上的内容是什么，这些如果没有通过 App Intents、Entity Schemas、View Annotations 讲清楚，后面再强的 Siri 和 Agent 也很难真正帮用户完成任务。

---

## 六、开发者不可忽略的其他更新

### Music Understanding

全新的音频分析框架，在设备端对音频进行**六维度分析**。无需网络、不依赖服务端，直接在 App 内做音频理解。适合音乐类、教育类、播客类应用。

### NowPlaying

统一播放信息出口，连接 **锁屏、控制中心、灵动岛、CarPlay**。过去各管各的播放控件，现在一套框架搞定。如果你在做音视频 App，这个迁移可能比看起来更值得。

### Game Porting Toolkit 4

移植工具包的第四次大版本更新，这次直接开放了**开源的 Agent 化移植技能**——把 Metal 和游戏移植的最佳实践做成了可复用的 AI 技能，移植效率再上一个台阶。

### Core Image RAW v9

RAW 格式图像处理引擎的重大升级，官方描述是「画质显著提升，清晰度和色彩表现都有实质飞跃」。

---

## 写在最后

回顾历届 WWDC，每一年的重点都不同：2019 年是 SwiftUI 的诞生，2020 年是 Apple Silicon 的宣告，2023 年是 Vision Pro 的亮相。

WWDC26 的核心信号很清楚：**AI 在苹果生态里的角色，从应用层的 Feature，变成了系统级的基础设施**。

Foundation Models 统一了系统模型、云端模型和自定义 Provider 的调用入口；Core AI 则面向自有模型的设备端部署。App Intents 的升级，用 AI 能力重新定义了 App 如何与系统交互。而 Xcode 27 的 Coding Agents，直接让 AI 坐到了你旁边的工位上。

这不是 AI 抢饭碗的老话题——这是一种新的开发范式的开端。掌握它，比抵制它更务实。

---

*本文首发于微信公众号「iOS观之」（微信号：run88184），欢迎关注。*
