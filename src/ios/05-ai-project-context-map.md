---
title: 如何让 AI 理解你的 iOS / Flutter 项目？组件地图、项目索引和 AGENTS.md
cover: ../assets/cover-coding-agent-ios.png
---

# 如何让 AI 理解你的 iOS / Flutter 项目？组件地图、项目索引和 AGENTS.md

> 真正影响 Coding Agent 效果的，往往不是某一句 Prompt 写得够不够漂亮，而是它能不能快速理解你的项目：组件怎么复用、业务怎么分层、Flutter 和 iOS 原生边界在哪里、哪些旧代码不能模仿。

---

## 前言

很多人用 AI 写代码时，会遇到一个重复的问题：

> 每次都要让它重新熟悉项目。
>
> 每次都要提醒它组件怎么用。
>
> 每次都要告诉它哪些代码不能改。

如果项目很小，这还可以忍。但真实的 iOS / Flutter 项目通常不是这样。它可能有原生壳、Flutter Module、多个业务模块、Repository、网络层、路由表、MethodChannel、历史遗留页面，还有团队自己的代码规范。

这时候，继续靠一句「你先熟悉一下项目」是不够的。

更好的做法是：给 AI 准备一套长期可复用的项目上下文。

---

## 一、新项目：先建立组件地图

新项目最怕的是每个页面都让 AI 重新造一套组件。

今天它生成一个按钮，明天又生成一个空状态，后天再生成一个 loading 组件。每一段代码单独看都没问题，但合在一起，UI 风格和架构边界就散了。

所以新项目一开始就应该建立一份 `docs/component-map.md`。

组件地图不是源码合集，而是一份索引。它告诉 AI：项目里有哪些通用组件、分别负责什么、什么时候应该复用、哪些只是历史遗留。

例如：

- `PrimaryButton`：主按钮，支持 loading / disabled，用在登录、提交订单、确认支付
- `EmptyStateView` / `EmptyStateWidget`：空状态组件，传入 icon、title、description、action
- `ToastManager` / `ToastService`：统一提示入口，不允许页面直接创建临时 toast
- `UserRepository`：用户数据来源，负责登录态、用户信息、token 刷新
- `OrderListPage`：订单列表页，依赖 `OrderListController` 和 `OrderRepository`

之后再让 AI 写页面时，不要让它自由发挥，而是要求它先读组件地图。

一个可用的 Prompt 是：

```
请阅读当前项目的 UI 组件、页面和状态管理代码，生成 docs/component-map.md。

要求：
1. 只总结，不修改业务代码。
2. 按 UI 组件、页面、状态管理、Repository、平台桥接分类。
3. 每个条目说明职责、主要参数、典型使用场景。
4. 标记哪些组件是推荐复用的，哪些只是历史遗留。
5. 不要粘贴大段源码，只写索引和说明。
```

这份文档不需要一次写完。每新增一个通用组件，就让 AI 顺手更新它。

---

## 二、老项目：先做项目索引，不要马上改代码

老项目的问题不是没有上下文，而是上下文太多。

目录多、历史包袱多、命名不统一、相似页面一堆，AI 如果每次都从头扫，很容易浪费时间，也容易抓错重点。

这时候不要一上来就让 AI 改代码。先让它做项目索引。

项目索引可以放在 `docs/project-map.md`，内容包括：

- 目录结构和模块职责
- 主要业务链路
- 页面入口和路由表
- 网络层、Repository、缓存层关系
- Flutter Module 和 iOS 原生之间的边界
- MethodChannel / EventChannel 列表
- 常见组件和推荐写法
- 已知历史遗留和不要模仿的旧代码

一个适合老项目的 Prompt 是：

```
请先不要修改代码。

请阅读项目结构，生成 docs/project-map.md：
1. 总结主要模块和目录职责。
2. 标出 iOS 原生、Flutter Module、平台桥接分别在哪里。
3. 总结网络层、Repository、状态管理、路由的现有模式。
4. 找出 3-5 个最值得复用的页面或组件作为参考样板。
5. 标记明显的历史遗留写法，提醒后续不要模仿。
6. 文档只写索引和说明，不粘贴大段源码。
```

这一步看起来像是在「写文档」，但实际是在降低后续每一次 AI 协作的成本。

---

## 三、AGENTS.md：把反复说的话固化下来

如果你发现同一类要求每次都要重复说，就不应该继续靠手写 Prompt 解决。

比如：

- Flutter JSON 解析必须使用 `g_json`
- 列表必须使用 `ListView.builder`
- `TextStyle` 必须显式设置 `color`
- UI 不直接调用 API
- 所有数据通过 Repository 获取
- MethodChannel 只做桥接，不写业务 UI 逻辑
- iOS 原生和 Flutter 路由边界不能混用

这些应该写进 `AGENTS.md` 或项目文档里，让 Agent 每次自动读到。

`AGENTS.md` 可以写得很具体：

```
## Flutter 规范

- JSON 解析必须使用 g_json。
- 列表必须使用 ListView.builder。
- TextStyle 必须显式设置 color。
- UI 层禁止直接调用 API。
- 所有数据通过 Repository 获取。

## iOS / Flutter 边界

- MethodChannel 只做桥接，不写业务 UI 逻辑。
- Flutter 不直接依赖 iOS 原生页面内部实现。
- iOS 原生跳转 Flutter 页面必须走统一 Router。
- Deep Link 必须同时验证冷启动、登录态和 Flutter engine 未初始化场景。
```

临时 Prompt 是一次性的，项目规则才是可复用的。

---

## 四、后续任务：只读相关文件，不要全量扫描

有了 `AGENTS.md`、`docs/project-map.md`、`docs/component-map.md` 之后，后续任务就不应该再让 AI 全量扫描项目。

更好的任务写法是：

```
请先阅读 AGENTS.md、docs/project-map.md、docs/component-map.md。

然后参考现有 OrderListPage 的写法，实现 RefundListPage。

限制：
1. 只读取和本任务直接相关的文件。
2. 不要全量扫描项目。
3. 不要新增通用组件，除非先说明原因。
4. 不修改路由表以外的全局配置。
5. 修改前先列出计划和涉及文件。
```

这比每次都说「你先熟悉一下整个项目」稳定得多。

AI 不需要每次重新认识所有东西。它需要的是一份稳定的索引，以及明确的任务边界。

---

## 五、组件地图和项目索引要持续维护

组件地图和项目索引不是一次性文档。

如果它们写完就不管，很快也会变成过期文档。正确做法是把维护动作放进日常工作流：

- 新增通用组件后，更新 `docs/component-map.md`
- 新增业务模块后，更新 `docs/project-map.md`
- 改了路由或桥接方式后，更新对应说明
- 遇到 AI 反复犯同一个错，把规则补进 `AGENTS.md`
- Code Review 时顺手检查文档是否需要同步

这件事的目标不是写一堆漂亮文档，而是让 AI 和人都能更快进入项目。

---

## 六、AI 越强，越需要工程规则

很多人会觉得，等 AI 更强了，它自然就能理解项目，不需要这些文档。

我反而觉得相反。

AI 越强，越能一次性改更多文件，越能自己规划更长的任务链路，也就越需要明确的边界。否则它不是写得更好，而是错得更远。

以后开发者要做的，不只是写 Prompt，而是定义工程系统：

- 用 `AGENTS.md` 固化项目规则
- 用 `project-map` 降低理解成本
- 用 `component-map` 约束复用方式
- 用 lint 和测试兜住质量
- 用 CI 和 checklist 约束上线流程

这样 AI 越强，项目越受益；而不是 AI 越能写，项目越失控。

---

## 参考资料与延伸阅读

- OpenAI Developers：[Codex best practices](https://developers.openai.com/codex/learn/best-practices)  
  重点看「Context and prompts」「Plan first」「AGENTS.md」。

- OpenAI Developers：[Codex prompting](https://developers.openai.com/codex/prompting)  
  官方说明了为什么要给 agent 提供相关文件、上下文和明确任务边界。

- Flutter Docs：[Platform channels](https://docs.flutter.dev/platform-integration/platform-channels)  
  处理 Flutter 与 iOS 原生桥接时，MethodChannel / EventChannel 的基础资料。

---

## 写在最后

让 AI 理解项目，不是靠一次全量扫描，也不是靠一句「你先熟悉一下」。

更可靠的方式，是把项目变成 AI 能持续理解的形态：有组件地图，有项目索引，有 AGENTS.md，有测试和规则。

当这些东西建立起来之后，Coding Agent 才不只是一个会写代码的工具，而是一个能在项目边界内稳定工作的协作者。

---

*本文首发于微信公众号「iOS观之」（微信号：run88184），欢迎关注。*
