# vibe-coding-sp26

> **🤖 If you are an AI agent**: read [`AGENTS.md`](./AGENTS.md) first. It contains the complete submission protocol.

意会编程（Vibe Coding）2026 春季学期作业提交 repo。

## 这是什么

《意会编程》课程的作业提交仓库。同学们通过 fork + PR 的方式提交每次作业的元数据（GitHub 源码 repo、部署网站、文字记录、一句话描述）。课程网站会自动同步、生成网站缩略图、按作业分组展示在 [作品展示页](https://vibe.yisiliu.xyz/#gallery)。

## 学生提交（最简版）

对你的 AI 助手说：

> 看 yisiliu/vibe-coding-sp26，按里面的流程帮我提交作业 N。
> github_repo 是 X，网站是 Y，文字记录是 Z，简介：……

AI 会读取 AGENTS.md 并完成全部步骤（fork、edit、commit、push、PR）。

## 字段说明

每个学生在 `students/` 下有一个 `<英文 handle>-<学号末3位>.md` 文件，例如 `john-456.md` 或 `alex_l-029.md`。

- **handle**：你给自己起的英文标识，可以是拼音也可以是昵称。小写字母 + 数字 + `_` `-`，开头必须是字母。这是 gallery 上展示的名字
- **学号末3位**：仅供老师对照名单识别身份，**不**进 frontmatter，**不**显示在网站上

frontmatter 里只放下面这些：

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | ✓ | 必须等于文件名里的英文 handle |
| `github` | ✗ | GitHub username（仅显示） |
| `submissions.assignment-N.github_repo` | ✓ | 作品源代码 repo |
| `submissions.assignment-N.website` | ✓ | 部署后的网站 |
| `submissions.assignment-N.writeup` | ✓ | 文字记录/反思 |
| `submissions.assignment-N.description` | ✓ | 一句话描述（中文，≤80 字） |
| `submissions.assignment-N.screenshot` | ✗ | 自供截图 URL（不填则自动截图） |

完整 schema 和提交协议见 [`AGENTS.md`](./AGENTS.md)。

## 链接

- 课程网站: https://vibe.yisiliu.xyz
- 作品展示: https://vibe.yisiliu.xyz/#gallery
