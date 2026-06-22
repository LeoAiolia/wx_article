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
