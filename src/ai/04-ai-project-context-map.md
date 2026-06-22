---
title: AI Coding 移动端工程实践（二）：如何让 AI 理解你的项目？
cover: ../assets/cover-coding-agent-ios.png
---

# AI Coding 移动端工程实践（二）：如何让 AI 理解你的项目？

> 真正影响 Coding Agent 效果的，不只是 Prompt，而是它能不能快速理解你的项目。

---

## 前言

很多人每次用 AI 都要重新说一遍：

> 这个项目怎么分层。
>
> 哪些组件能复用。
>
> 哪些旧代码不要模仿。

这说明项目缺少一份 AI 能读懂的长期上下文。

---

## 一、新项目：建立组件地图

新项目最怕每个页面都让 AI 重新造组件。

建议尽早建立 `docs/component-map.md`：

- `PrimaryButton`：主按钮，支持 loading / disabled
- `EmptyStateWidget`：空状态组件
- `ToastService`：统一提示入口
- `UserRepository`：用户数据和登录态
- `OrderListPage`：订单列表页样板

组件地图不是源码合集，而是索引。它告诉 AI：哪些组件应该复用，哪些不要再造。

---

## 二、老项目：建立项目索引

老项目上下文太多，AI 每次全量扫描成本很高，也容易抓错重点。

可以建立 `docs/project-map.md`：

- 目录结构和模块职责
- 主要业务链路
- 页面入口和路由表
- 网络层、Repository、缓存层关系
- Flutter Module 和 iOS 原生边界
- MethodChannel / EventChannel 列表
- 推荐复用的页面或组件
- 不要模仿的历史遗留写法

后续任务先读索引，再读相关文件。

---

## 三、把规则写进 AGENTS.md

反复强调的规则，不要每次都写在 Prompt 里。

比如：

- Flutter JSON 解析必须使用 `g_json`
- 列表必须使用 `ListView.builder`
- `TextStyle` 必须显式设置 `color`
- UI 不直接调用 API
- 数据通过 Repository 获取
- MethodChannel 只做桥接，不写业务 UI 逻辑

这些规则应该写进 `AGENTS.md`。

---

## 四、避免每次全量扫描

后续任务可以这样写：

```
请先阅读 AGENTS.md、docs/project-map.md、docs/component-map.md。
然后参考现有 OrderListPage，实现 RefundListPage。
只读取和本任务直接相关的文件，不要全量扫描项目。
修改前先列计划和涉及文件。
```

这比「你先熟悉一下整个项目」稳定得多。

---

## 五、区分规则、索引和记忆

项目上下文不要全部塞进一个文件。

可以这样分：

- `AGENTS.md`：给 Codex / 通用 agent 看的项目规则
- `CLAUDE.md`：给 Claude Code 看的项目规则和工作流
- `docs/project-map.md`：项目结构索引
- `docs/component-map.md`：组件索引
- 自动记忆 / memory：工具自己记录的偏好和发现

这里要注意：记忆和说明文件只是上下文，不是强制安全边界。真正不允许做的事情，比如删除文件、修改证书、读取敏感目录，应该靠权限、hooks、CI 和人工确认兜住。

---

## 参考资料与延伸阅读

- OpenAI Developers：[Codex best practices](https://developers.openai.com/codex/learn/best-practices)
- OpenAI Developers：[Codex prompting](https://developers.openai.com/codex/prompting)
- Anthropic Docs：[How Claude remembers your project](https://docs.anthropic.com/en/docs/claude-code/memory)

---

## 写在最后

让 AI 理解项目，不是靠一次全量扫描，而是靠可持续维护的上下文。

组件地图、项目索引、AGENTS.md，本质上都是在把团队经验变成 AI 可读取的工程资产。

---

*本文首发于微信公众号「iOS观之」（微信号：run88184），欢迎关注。*
