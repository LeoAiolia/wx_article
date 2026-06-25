---
title: Agent Skills 和 MCP 到底有什么区别？一文讲透 AI 编程的两大扩展机制
cover: ../assets/cover-skills-vs-mcp.jpeg
---

# Agent Skills 和 MCP 到底有什么区别？一文讲透 AI 编程的两大扩展机制

> Skills 是大脑，MCP 是双手。一个教 AI 怎么思考，一个给 AI 做事的能力。两者不是替代关系，而是互补层。

---

## 前言

2026 年的 AI 编程工具生态，有两个词你绕不开：**Skills** 和 **MCP**。

GitHub 上 Skills 仓库已经超过 1400 个，MCP 服务器突破 2 万个。但很多人还是分不清——这东西到底是干什么的？我该装 Skills 还是配 MCP？为什么有人写了 40 小时的 MCP Server，结果被一个 10 分钟的 SKILL.md 替代了？

这篇文章从架构层面把两者的区别讲清楚。

---

## 一、先看一个场景

假设你要让 AI 帮你做 Code Review。

**用 Skills 怎么做？**

写一个 `SKILL.md`，告诉 AI：

```markdown
# Code Review Skill
1. 先检查命名规范
2. 再检查错误处理
3. 最后检查性能问题
4. 输出按严重程度分级：Critical / Major / Minor
```

AI 读到这份"标准作业程序"，就知道按什么流程审代码。

**用 MCP 怎么做？**

写一个 MCP Server，暴露工具给 AI 调用：

```
工具1: get_pr_diff(pr_id) → 拉取 PR 变更
工具2: post_review_comment(pr_id, file, line, comment) → 发表评论
工具3: get_file_blame(file, line) → 查谁写的这行
```

AI 自己决定调用哪个工具、什么顺序、怎么组合。

**看出区别了吗？** Skills 定义的是「流程」，MCP 提供的是「能力」。

---

## 二、本质区别：软编排 vs 硬编排

这是两者最核心的架构哲学差异。

| 维度 | Skills | MCP |
|---|---|---|
| **本质** | 声明式知识包（Markdown + 脚本） | 通信协议标准（JSON-RPC） |
| **编排方式** | **软编排**：逻辑在 Prompt 里，AI 可见每步推理 | **硬编排**：逻辑在代码里，AI 只能看到输入输出 |
| **运行时** | 注入当前会话上下文，无独立进程 | 独立进程，跨进程通信 |
| **决策者** | AI 模型在运行时动态判断 | 开发者在编码时预先定义 |
| **Token 成本** | 元数据 30-50 token/个，激活后才加载完整指令 | 一个 5 服务器的配置可能吃掉 55K+ token |
| **开发门槛** | 会写 Markdown 就行 | 需要编程，处理认证、限流、错误 |
| **确定性** | 依赖模型质量，灵活但不可控 | 代码强制执行，高度可预测 |

一句话总结：

> **Skills 把业务逻辑交还给 AI 的大脑做实时编排；MCP 把关键能力封装成标准化接口，保证安全可控。**

---

## 三、类比：大脑 vs 双手

这是中文社区流传最广的类比，确实精准：

```
Skills  = 大脑 / SOP 手册 → 告诉 AI「怎么做才对」
MCP     = 双手 / 工具    → 给 AI「做事的能力」
Agent   = 灵魂 / 角色    → 定义 AI「是谁、负责什么」
```

- 你给 AI 一本《代码审查 Checklist》→ 这是 **Skill**
- 你给 AI 接上 GitHub API，让它能真正去 PR 下面评论 → 这是 **MCP**
- 你定义这个 AI 是「高级工程师，负责代码质量把关」→ 这是 **Agent 角色**

三者各司其职，不是互相替代。

---

## 四、性能实测：MCP 不一定更快

2026 年 5 月，Arize 做了一个 500 次试验的对比评测，结果有点反直觉：

| 指标 | MCP | Skill（短） | Skill（长） | 裸 Claude |
|---|---|---|---|---|
| **正确率** | 83.4% | 83.3% | 82.6% | 84.5% |
| **成本（最难任务）** | **6 倍** | 基准线 | 略高 | 略高 |
| **延迟（最难任务）** | **5 倍** | 基准线 | 更长 | 更长 |
| **工具忠实度** | 33%（经常逃逸到 bash） | >99% | >99% | N/A |

**核心发现：**

对于 GitHub 这种已有成熟 CLI 的场景，Skills 反而比 MCP 更快更省钱。原因是 Skills 让 AI 直接用 `gh` 命令 + `grep` / `jq` 组合——这是命令行天生的灵活性；而 MCP 的固定 API 表面做不到这种自由组合。

但 MCP 的不可替代之处在于：**认证/授权** 和 **消费者友好**——普通人不需要装 CLI 就能用。

> 结论：**已知 CLI 的工具，用 Skills 封装更高效；需要复杂认证或对外分发的，走 MCP。**

---

## 五、什么时候用 Skills？什么时候用 MCP？

### 选 Skills 的场景

- 定义编码规范、Code Review 流程
- 封装团队最佳实践（部署检查清单、API 设计规范）
- 文档生成、PPT 制作等模板驱动型任务
- 多步骤工作流编排（先分析 → 再设计 → 最后实现）
- 团队没有后端资源，需要快速验证想法
- **一句话：任务是「教 AI 怎么思考」**

### 选 MCP 的场景

- 对接 GitHub / GitLab（PR、Issue、CI）
- 连接数据库（只读查询、数据分析）
- 浏览器自动化（Playwright、Puppeteer）
- 调用内部 API（部署系统、监控平台）
- 需要企业级权限控制和安全审计
- **一句话：任务是「让 AI 能触碰外部世界」**

### 两者组合（推荐）

实际项目中，成熟团队的做法是组合：

```
Layer 3: Skills     → 定义流程和知识（/review、/deploy-check）
Layer 2: Sub-Agent  → 专项隔离执行（code-reviewer、debugger）
Layer 1: MCP        → 提供外部连接（GitHub、数据库、部署管线）
```

Skills 负责「要做什么、按什么标准做」，MCP 负责「拿到数据、执行动作」。

---

## 六、一个反例：别把 Skill 写成 MCP，也别把 MCP 写成 Skill

社区里最常见的两个错误：

**错误 1：为静态内容写 MCP Server**

有开发者花了 40 小时写了一个 MCP Server，功能是把公司编码规范传给 AI。后来发现——写一个 `SKILL.md`，10 分钟搞定，效果一样。

> MCP 是为**有状态的、需要外部交互**的场景设计的。静态知识直接用 Skills。

**错误 2：在 Skill 里写「查询数据库」**

Skill 是纯文本指令，它不能自己执行外部操作。如果你在 SKILL.md 里写「先查数据库拿到用户列表」——AI 做不到，因为它没有数据库连接。

> 涉及外部系统、实时数据、API 调用 → 必须走 MCP。

---

## 七、一张图总结

```
┌──────────────────────────────────────────────┐
│                  AI Agent                     │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │  Skills  │  │  MCP     │  │  Sub-Agent │  │
│  │          │  │          │  │            │  │
│  │ 怎么做   │  │ 能做什么  │  │  谁来做    │  │
│  │ 流程/知识│  │ 工具/连接 │  │  角色/隔离 │  │
│  │          │  │          │  │            │  │
│  │ Markdown │  │ 独立进程  │  │  独立会话  │  │
│  │ Token 省 │  │ 安全可控  │  │  专注执行  │  │
│  └──────────┘  └──────────┘  └────────────┘  │
└──────────────────────────────────────────────┘
```

- 写 Markdown → Skills
- 接外部系统 → MCP
- 两者都配 → 完整 Agent

---

## 小结

Skills 和 MCP 不是二选一，而是 AI 编程工具栈的两个正交维度：

- **Skills** 解决「知识注入」问题——让 AI 懂你的业务、守你的规范
- **MCP** 解决「能力扩展」问题——让 AI 能真正操作外部世界

真正高效的 AI 编程 setup，一定是两者配合：用 Skills 定义流程和标准，用 MCP 获取实时数据和执行动作。

下次有人问你「Skills 和 MCP 哪个更好」，你可以告诉他：**这不是哪个更好的问题，而是你缺大脑还是缺双手的问题。**

---

## 参考资料

- [Claude Code Skills vs MCP vs Plugins: Complete Guide 2026](https://www.morphllm.com/claude-code-skills-mcp-plugins)
- [MCP vs. CLI Skills for agents: what our eval found](https://arize.com/blog/mcp-vs-cli-skills-for-agents-what-our-eval-found-and-which-you-should-use/)
- [从 MCP 到 Agent Skills：AI 工具生态演进中的能力供给范式对比](https://developer.baidu.com/article/detail.html?id=7244281)
- [Agent Skills 与 MCP：一场被误解的「替代战争」](https://developer.jdcloud.com/article/4436)
- [Claude Code 源码解读：插件、Skills 与 MCP——三层扩展体系](https://blog.csdn.net/bhl120/article/details/160006035)
