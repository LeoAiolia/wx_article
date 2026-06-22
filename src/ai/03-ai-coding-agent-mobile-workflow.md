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

## 一、适合交给 AI 的事情

适合交给 AI 的任务，通常有三个特点：边界清楚、模式固定、容易验证。

比如：

- SwiftUI / Flutter 页面骨架
- Model / DTO / Repository 样板代码
- ViewModel / Controller 的基础状态流
- 单元测试和 mock 数据
- 小范围重构
- crash log / Dart analyze 报错分析
- README 和迁移说明

这些工作不一定要全部手写。AI 可以帮你把第一版搭出来，人再负责审查和收口。

---

## 二、不适合直接甩给 AI 的事情

下面这些事情不能一句话交给 AI：

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

## 四、让 AI 先出方案

稍微复杂的任务，不要直接让 AI 改代码。

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

比如 Xcode 的 agentic coding 已经可以结合 Xcode 能力去构建项目、运行测试、搜索 Apple 文档。Claude Code 这类工具也能读代码、改文件、运行命令。

这很好，但不代表应该默认放开所有权限。

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
