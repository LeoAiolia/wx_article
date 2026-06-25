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

- 全局习惯放在你自己的全局规则目录或工具全局配置里
- 项目规则在项目内维护一份规则源，比如 `AGENTS.md`
- 业务上下文放 `docs/project-map.md`
- 组件说明放 `docs/component-map.md`

重点不是文件名必须统一，而是作用域要分清楚。不要把所有东西都塞进一个文件。

比如你可以把自己的通用习惯单独放在一个目录：

```
~/rule/AGENTS.md
```

里面写回复语言、Git 偏好、代码审查风格、危险命令限制等全局习惯。如果使用 Claude Code，可以在全局或项目 `CLAUDE.md` 里引用它：

```
@~/rule/AGENTS.md
```

这样全局习惯仍然只维护一份，具体项目再维护自己的项目规则。

| 层级 | 放在哪里 | 内容 | 范围 |
|------|----------|------|------|
| 全局 | 全局规则目录 / 工具全局配置 | 回复语言、工作方式、个人偏好 | 所有项目 |
| 项目 | 项目内规则源，比如 `AGENTS.md` | 技术栈约束、架构规则 | 当前项目 |
| 业务 | `docs/project-map.md` | 模块职责、接口说明 | 当前项目 |

![AI Coding 项目规则分层示意](../assets/inline-ai-05-rules-system.png)

> 不同工具的规则入口不同——Claude Code 常用 `CLAUDE.md`，Cursor 用 `.cursorrules`（正迁移到 `.cursor/rules/`），GitHub Copilot 读 `.github/copilot-instructions.md`。更稳的做法是把项目规则维护成一份稳定的规则源，比如 `AGENTS.md`，再让不同工具通过自己的入口文件引用或同步它。使用 Claude Code 时，也可以在项目 `CLAUDE.md` 里通过 `@` 引用全局规则文件或项目规则文件。

---

## 二、全局规则适合放什么

全局规则更适合放个人或团队通用习惯：

- 回复语言
- 是否先给计划
- 是否自动跑测试
- Git 操作偏好
- 不允许执行的危险命令
- 代码审查输出风格

这些规则和具体项目关系不大，换项目也成立。至于它具体放在 `CLAUDE.md`、某个全局 rule 目录，还是工具自己的全局配置里，可以按你实际使用的工具来定。

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

最常见的问题是：全局规则写一遍，项目规则又复制一遍。

重复会带来两个风险：

- 改一处忘了改另一处
- 两边规则冲突，AI 不知道听谁的

更好的做法是分层：

- 全局只写工作方式
- 项目只写项目规则
- 文档只写业务上下文

具体落地时，推荐一个简单模式：**项目规则只维护一份项目内规则源**。比如用 `AGENTS.md` 放项目规则，然后在 Claude Code 的项目 `CLAUDE.md` 里用 `@AGENTS.md` 引用它；如果你还有一套全局 rule 目录，也可以在 Claude Code 入口文件里用 `@` 引用其中的具体规则文件，比如 `@~/rule/AGENTS.md`。其他工具（Cursor、GitHub Copilot 等）也通过各自的规则文件指向同一份项目规则，避免多文件漂移。

如果全局规则和项目规则确实冲突了（比如全局要求英文回复，但项目是中文项目），优先级很简单：**项目规则 > 全局规则**，越具体者越优先。

---

## 五、规则不是权限控制

规则文件适合告诉 AI「应该怎么做」，但不适合承担安全边界。

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
| 工具入口文件 | 按需 | 个人偏好或工具适配，团队可协商要不要统一 |
| `docs/project-map.md` | ✅ 入 | 业务上下文，团队共享 |

`AGENTS.md` 一定要进版本控制——它是项目的 AI 协作约定，和 `README.md` 一样属于项目文档的一部分。

---

## 八、规则写到多细合适

这是实践中最容易踩的坑。太粗了没效果（比如"代码写好一点"），太细了 AI 记不住也不遵守。

两条原则可以参考：

- **可验证原则**：每条规则应该能被检查——要么 AI 能自查，要么 Code Review 能一眼识别。比如「列表必须使用 `ListView.builder`」可验证，「代码要优雅」不可验证。
- **频率原则**：AI 在同一类场景下 ≥3 次犯同一个错，才值得固化为规则。偶尔一次可能是上下文问题，不值得写进规则文件。

可以简单对比一下：

| 不建议这样写 | 建议这样写 |
|--------------|------------|
| 代码写优雅一点 | UI 层禁止直接调用 API，数据必须通过 Repository 获取 |
| 注意性能 | 长列表必须使用 `ListView.builder`，禁止一次性渲染完整列表 |
| JSON 解析要规范 | JSON 解析必须使用 `g_json`，不要手写 Map 取值 |
| 不要乱改配置 | 未经确认不要修改 Podfile、签名配置、路由表和全局网络封装 |
| 多写点测试 | ViewModel 状态变化和 Repository 错误分支必须补测试 |

好规则通常有三个特点：能判断、能执行、能在 review 里被指出。坏规则往往只表达愿望，AI 看完也不知道具体该怎么做。

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
