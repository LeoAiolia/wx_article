---
title: AI Coding 移动端工程实践（三）：AGENTS.md、CLAUDE.md 和项目规则该怎么写？
cover: ../assets/cover-coding-agent-ios.png
---

# AI Coding 移动端工程实践（三）：AGENTS.md、CLAUDE.md 和项目规则该怎么写？

> AI 写代码之前，应该先知道项目规则。规则写在哪里，比 Prompt 写得多漂亮更重要。

---

## 前言

很多 AI Coding 问题，不是模型不够强，而是规则没有沉淀。

你每次都提醒它：

- 不要直接调 API
- JSON 解析用指定工具
- 列表用懒加载
- 不要乱改路由
- 不要动全局配置

这说明这些要求不该只放在聊天里，而应该变成项目规则。

---

## 一、全局规则和项目规则分开

如果你同时用 Claude Code、Codex、Cursor 等工具，很容易出现规则重复。

一个简单原则：

- 全局习惯放 `CLAUDE.md` 或工具全局配置
- 项目规则放 `AGENTS.md`
- 业务上下文放 `docs/project-map.md`
- 组件说明放 `docs/component-map.md`

不要把所有东西都塞进一个文件。

| 层级 | 文件 | 内容 | 范围 |
|------|------|------|------|
| 全局 | `~/.claude/CLAUDE.md` | 回复语言、工作方式 | 所有项目 |
| 项目 | `AGENTS.md` | 技术栈约束、架构规则 | 当前项目 |
| 业务 | `docs/project-map.md` | 模块职责、接口说明 | 当前项目 |

> 不同工具的规则文件名不同——Claude Code 读 `CLAUDE.md`，Cursor 用 `.cursorrules`（正迁移到 `.cursor/rules/`），GitHub Copilot 读 `.github/copilot-instructions.md`。但 `AGENTS.md` 是你自己写的项目规则，把核心内容放在这里，再让各工具用自己的机制去引用它，一份文件覆盖所有工具。

---

## 二、CLAUDE.md 适合放什么

`CLAUDE.md` 更适合放个人或团队通用习惯：

- 回复语言
- 是否先给计划
- 是否自动跑测试
- Git 操作偏好
- 不允许执行的危险命令
- 代码审查输出风格

这些规则和具体项目关系不大，换项目也成立。

---

## 三、AGENTS.md 适合放什么

`AGENTS.md` 应该写项目专属规则。

比如 Flutter 项目：

```
## Flutter 规则

- JSON 解析必须使用 g_json。
- 列表必须使用 ListView.builder。
- TextStyle 必须显式设置 color。
- StreamSubscription 必须在 dispose 中释放。
- UI 层禁止直接调用 API。
- 所有数据通过 Repository 获取。
```

比如 iOS / Flutter 混合项目：

```
## 跨端边界

- MethodChannel 只做桥接，不写业务 UI 逻辑。
- iOS 原生跳转 Flutter 页面必须走统一 Router。
- Deep Link 必须验证冷启动、登录态、Flutter engine 未初始化场景。
```

---

## 四、避免重复规则

最常见的问题是：`CLAUDE.md` 写一遍，`AGENTS.md` 又写一遍。

重复会带来两个风险：

- 改一处忘了改另一处
- 两边规则冲突，AI 不知道听谁的

更好的做法是分层：

- 全局只写工作方式
- 项目只写项目规则
- 文档只写业务上下文

具体落地时，推荐一个简单模式：**项目规则只维护 `AGENTS.md` 一份**。如果你用 Claude Code，在项目 `CLAUDE.md` 里只写一行 `@AGENTS.md`，让 Claude 自动读取项目规则，不需要把同样内容复制两份。其他工具（Cursor、GitHub Copilot 等）也可以直接读 `AGENTS.md`，一份文件覆盖多个 AI 工具，避免多文件漂移。

如果全局规则和项目规则确实冲突了（比如全局要求英文回复，但项目是中文项目），优先级很简单：**项目规则 > 全局规则**，越具体者越优先。

---

## 五、规则不是权限控制

`AGENTS.md` 和 `CLAUDE.md` 适合告诉 AI「应该怎么做」，但不适合承担安全边界。

比如下面这些，不应该只靠文档约束：

- 不允许删除文件
- 不允许读取密钥
- 不允许修改证书和发布配置
- 不允许执行危险命令
- 不允许自动提交或推送

这些要靠工具权限、hooks、CI、代码审查和人工确认。

Claude Code 官方也把权限和 hooks 当成单独能力：读文件、改文件、运行命令、自动格式化、阻止受保护文件修改，都应该放在工具层面控制，而不是只写一句「不要这样做」。

---

## 六、什么时候更新规则

以下情况应该更新规则：

- AI 反复犯同一个错
- Code Review 发现同类问题重复出现
- 新增通用组件
- 改了网络层或路由方式
- 引入新的状态管理方案
- Flutter 和原生边界发生变化

规则不是一次写完，而是随着项目演进持续维护。

---

## 七、规则文件该不该进版本控制

简单结论：

| 文件 | 是否入 Git | 原因 |
|------|-----------|------|
| `AGENTS.md` | ✅ 入 | 项目规则，全员共享 |
| `CLAUDE.md` | 按需 | 个人偏好，团队可协商要不要统一 |
| `docs/project-map.md` | ✅ 入 | 业务上下文，团队共享 |

`AGENTS.md` 一定要进版本控制——它是项目的 AI 协作约定，和 `README.md` 一样属于项目文档的一部分。

---

## 八、规则写到多细合适

这是实践中最容易踩的坑。太粗了没效果（比如"代码写好一点"），太细了 AI 记不住也不遵守。

两条原则可以参考：

- **可验证原则**：每条规则应该能被检查——要么 AI 能自查，要么 Code Review 能一眼识别。比如「列表必须使用 `ListView.builder`」可验证，「代码要优雅」不可验证。
- **频率原则**：AI 在同一类场景下 ≥3 次犯同一个错，才值得固化为规则。偶尔一次可能是上下文问题，不值得写进规则文件。

规则不是越多越好，少而精准的规则比一长串没人看的规则有效得多。

---

## 参考资料与延伸阅读

- OpenAI Developers：[Codex best practices](https://developers.openai.com/codex/learn/best-practices)
- Anthropic Docs：[How Claude remembers your project](https://docs.anthropic.com/en/docs/claude-code/memory)
- Anthropic Docs：[Claude Code security](https://docs.anthropic.com/en/docs/claude-code/security)
- Anthropic Docs：[Automate actions with hooks](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)

---

## 写在最后

Prompt 解决一次任务，规则解决一类问题。

AI Coding 真正成熟的标志，不是你会写很长的提示词，而是项目有清晰、稳定、可复用的规则系统。

---

*本文首发于微信公众号「iOS观之」（微信号：run88184），欢迎关注。*
