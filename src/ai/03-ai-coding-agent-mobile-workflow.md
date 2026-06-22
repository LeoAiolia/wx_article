---
title: AI Coding 移动端工程实践（一）：iOS / Flutter 开发者该怎么用好 Coding Agent？
cover: ../assets/cover-coding-agent-ios.png
---

# AI Coding 移动端工程实践（一）：iOS / Flutter 开发者该怎么用好 Coding Agent？

> Coding Agent 不是「替你写 App 的外包」，而是一个需要明确指挥、严格验收的开发助手。

---

## 前言

AI 已经能写很多代码，但移动端项目不是 demo。真实项目里有 iOS 原生、Flutter Module、证书签名、路由、登录态、MethodChannel、线上兼容和真机体验。

所以问题不是「要不要用 AI」，而是：**怎么把 AI 放进可控的工程流程里。**

---

## 工具箱速览

在讨论工作流之前，先看清工具箱里有什么。

### Xcode 内置（26.3+）

从 Xcode 26.3 起，Apple 原生集成了 agentic coding——AI 代理可以直接读取项目结构、搜索 Apple 文档、修改文件、构建修复、运行测试、操作 Preview 验证 UI。到 Xcode 27，进一步加入了 Plan Mode、多代理协作、Gemini 作为第三方模型选项。对 iOS 开发者来说，这是最「原生」的体验——不需要离开 IDE，AI 天然理解 Xcode 项目和 Apple 框架。

### 终端 / CLI 类

| 工具 | 特点 |
|------|------|
| **Claude Code** | Anthropic 出品，终端运行，也提供 VS Code / JetBrains 插件。在大型重构、多文件变更、安全审计上表现突出。支持 worktree 隔离 + 子代理并行。1M token 上下文窗口。 |
| **OpenAI Codex** | OpenAI 的终端代理，GPT-5 驱动，支持异步云端任务和 VS Code 插件。 |

### 编辑器 / IDE 类

| 工具 | 特点 |
|------|------|
| **Cursor** | 从 VS Code 分支出来的独立编辑器，底层重构了 AI 交互，补全体验比「VS Code + 插件」更流畅。支持多模型切换。 |
| **GitHub Copilot** | 覆盖面最广，VS Code、JetBrains、Xcode 均可使用。但代理能力落后于 Claude Code 和 Cursor。 |

> 对 iOS / Flutter 开发者而言，不管你用哪款工具，AI 可以帮你分析代码、运行 `flutter analyze`，但**最终编译和真机调试仍然要回到 Xcode**。

### 两条实际路线

不用纠结「哪个最好」，按你的工作习惯选一条：

- **Xcode 为主路线**：Xcode 内置 Agent 负责日常编码，终端工具（Claude Code / Codex）处理离线重构和复杂任务。
- **VS Code / Cursor 路线**：Flutter 开发或以 VS Code 为主的团队，用 Cursor 或 Copilot 做日常补全，Claude Code 处理深度任务，Xcode 只用来编译和真机调试。

关键不是选了哪个工具，而是**怎么控制它**——这是本文后面的重点。

---

## 一、适合交给 AI 的事情

适合交给 AI 的任务，通常有三个特点：边界清楚、模式固定、容易验证。

比如：

- SwiftUI / Flutter 页面骨架
- Model / DTO / Repository 样板代码
- ViewModel / Controller 的基础状态流
- Widget 树拆分和重构
- 单元测试和 Widget Test
- crash log / Dart analyze 报错分析
- 本地数据库建表 / 迁移脚本（Drift / Core Data / Room）

这些工作不一定要全部手写。AI 可以帮你把第一版搭出来，人再负责审查和收口。

---

## 二、不适合让 AI 直接动手的事情

反过来，不适合让 AI 直接动手的，正是那些边界模糊、没有固定模式、不容易验证的事情。这里要区分两种参与方式：**出方案、给建议** 和 **直接写代码、改配置**。下面这些事情，可以让 AI 分析问题、列出选项、对比优劣（见第四节），但**不要让 AI 直接动手**——因为改坏了你可能根本察觉不到：

- 架构选型
- StoreKit / 订阅 / 登录态 / Token 刷新
- Keychain 和敏感数据处理
- Flutter 与 iOS 原生桥接边界
- Deep Link 和复杂导航
- 证书、签名、构建配置
- 动画、Haptic、键盘、页面切换手感

AI 可以给方案，但不能替你负责。

---

## 三、正确用法：小步、明确、可验收

不要说：

```
帮我写一个登录页。
```

应该说：

```
在现有 Flutter 项目中新增 LoginPage。
要求：
1. 只负责 UI，不直接调用 API。
2. 状态由 LoginController 提供。
3. 包含手机号、验证码、获取验证码、登录按钮。
4. loading 和 errorMessage 由外部状态控制。
5. JSON 解析遵守项目现有规范。
6. 不修改路由表和网络层。
```

任务越具体，AI 越不容易自由发挥。

---

## 四、复杂任务：先让 AI 出方案，再考虑动手

稍微复杂的任务，不要直接让 AI 改代码。包括第二节提到的架构选型、跨端方案选择等"高风险但适合讨论"的任务，都可以走这条路径。

先让它回答：

- 准备改哪些文件？
- 每个文件改什么？
- 为什么这么改？
- 有没有更小的拆分方式？

先看方案，再允许它动手。

---

## 五、每一步都要验证

AI 写完代码后，至少要检查：

- diff 有没有越界
- 编译是否通过
- `dart analyze` 是否干净
- `flutter test` 是否通过
- Xcode build 是否通过
- 真机关键路径是否正常

能跑，不等于正确。

---

## 六、不要忽略工具权限

Coding Agent 越能干，越要控制权限。

前面提到的工具，权限模型各不相同：Xcode 内置 Agent 深度集成 IDE，能改 entitlements、跑 build；Claude Code 和 Codex 作为终端工具，理论上可以操作文件系统里的任何东西。Copilot 作为编辑器插件权限相对受控，Cursor 作为独立编辑器介于二者之间。不论你用的是哪款，都不应该默认放开所有权限。

建议把权限分成几类：

- 读文件：通常可以放开
- 改文件：按任务允许
- 跑测试：可以允许，但要看命令
- 删除文件：必须确认
- 修改证书、配置、CI、发布脚本：必须确认
- 访问密钥、token、生产配置：默认禁止

AI 不是越自由越好。移动端项目里，签名、证书、Pod、Runner、CI、发布配置都属于高风险区域。

---

## 参考资料与延伸阅读

- Apple Developer：[Meet agentic coding in Xcode](https://developer.apple.com/videos/play/tech-talks/111428/)
- Anthropic Docs：[Claude Code security](https://docs.anthropic.com/en/docs/claude-code/security)

---

## 写在最后

AI Coding 的重点不是「让 AI 多写点」，而是让 AI 在正确边界里工作。

iOS / Flutter 开发者真正要守住的是：架构、跨端边界、体验、验证和上线质量。

---

*本文首发于微信公众号「iOS观之」（微信号：run88184），欢迎关注。*
