---
title: AI Coding 移动端工程实践（七）：从 Prompt 到工程系统
cover: ../assets/cover-coding-agent-ios.png
---

# AI Coding 移动端工程实践（七）：从 Prompt 到工程系统

> AI 越强，越不能只靠 Prompt。真正长期有效的是规则、文档、测试、CI 和发布流程。

---

## 前言

很多人刚开始用 AI Coding，会把重点放在 Prompt 上。

Prompt 当然重要，但它解决的是一次任务。

如果一个项目长期依赖 AI，真正重要的是工程系统。

---

## 一、Prompt 是入口，不是全部

Prompt 能告诉 AI 当前要做什么。

但它不适合承载所有规则：

- 项目架构
- 组件复用方式
- Flutter / iOS 边界
- 测试要求
- Git 提交规范
- 发布前 checklist

这些应该沉淀到项目里，而不是每次手写。

---

## 二、把规则变成文件

可以把规则分层：

- `AGENTS.md`：项目编码规则和 AI 协作规则
- `docs/project-map.md`：项目结构和模块职责
- `docs/component-map.md`：组件索引和复用说明
- `docs/release-checklist.md`：发布前检查项

这样 AI 和人都能复用同一套上下文。

---

## 三、把质量变成自动化

不要只靠人工提醒 AI：

- 列表必须懒加载
- JSON 解析必须走规范
- UI 不能直接调 API
- 测试必须补齐

能自动化的就自动化：

- lint
- `dart analyze`
- `flutter test`
- Xcode build
- 单元测试
- CI 检查

规则写在文档里，质量落在工具上。

---

## 四、把上线变成 checklist

AI 改完代码，不代表可以上线。

移动端发布前至少要看：

- 登录 / 支付 / 订阅
- 推送 / Deep Link
- Flutter / 原生跳转
- 真机体验
- 崩溃日志
- 权限弹窗
- App Store 审核风险

这些应该变成 checklist，而不是临时想起来才测。

---

## 五、AI 越强，越需要边界

未来 AI 会越来越能做长任务。

它会自己读代码、写方案、改文件、跑测试、修失败。

这当然是好事，但也意味着：如果边界不清楚，它一次造成的影响会更大。

所以未来开发者要做的，不只是写 Prompt，而是定义 AI 工作的工程边界。

---

## 六、把 LLM 风险纳入工程系统

AI Coding 还要考虑安全风险。

OWASP 的 LLM Top 10 里提到几个和开发工具强相关的问题：

- Prompt Injection：仓库里的文本、issue、日志可能诱导 AI 执行错误指令
- Insecure Output Handling：AI 生成的代码不能不审查就进入系统
- Sensitive Information Disclosure：不要把 token、证书、用户数据交给 AI
- Excessive Agency：不要给 AI 过大的自主权限
- Supply Chain Risk：AI 建议新增依赖时，要检查来源和维护状态

这些风险不是写一句「小心安全」就能解决的。

更现实的做法是：

- 限制 AI 权限
- 敏感信息脱敏
- 依赖变更必须人工确认
- 高风险文件加保护规则
- 所有 AI 生成代码都走 review 和测试

AI Coding 工程化，必须包含安全工程化。

---

## 参考资料与延伸阅读

- OWASP：[Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Anthropic Docs：[Claude Code security](https://docs.anthropic.com/en/docs/claude-code/security)
- Anthropic Docs：[Automate actions with hooks](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)

---

## 写在最后

AI Coding 的终点，不是人人都会写神奇 Prompt。

真正成熟的状态是：项目本身有清晰规则，AI 进入项目后知道该怎么做、不该怎么做、做完如何验证。

从 Prompt 到工程系统，这才是移动端开发真正需要补上的一课。

---

*本文首发于微信公众号「iOS观之」（微信号：run88184），欢迎关注。*
