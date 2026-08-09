# GitHub 项目文案学习报告

日期：2026-08-09

对象：`build-character-panel-skill` 的公开项目页与 README

## 一、我看了什么

这次只研究公开的 GitHub 一手项目文案，重点观察维护者如何在第一屏介绍产品、展示使用场景，以及如何把维护者说明和用户说明分开：

- [charmbracelet/gum](https://github.com/charmbracelet/gum)：用一句带性格的定位开场，然后马上给出可运行的小教程。
- [astral-sh/uv](https://github.com/astral-sh/uv)：先讲它替代什么、快在哪里，再给安装命令和真实终端输出。
- [shadcn-ui/ui](https://github.com/shadcn-ui/ui)：用一句“先拿来用，再改成自己的”说明产品关系，README 很短，把详细内容交给文档。
- [zed-industries/zed](https://github.com/zed-industries/zed)：先说“这是什么、谁做的”，再给下载入口；开发、贡献、授权分别放到后面。

## 二、成熟项目的共同写法

### 1. 第一行先回答“它能给我什么”

Gum 不是先解释目录结构，而是先说它能让 shell script 变漂亮，而且不用写 Go。uv 先说自己是 Python 包和项目管理器，并把“一个工具替代一串工具”列成亮点。shadcn/ui 则直接告诉读者：组件可以拿来改，最终变成自己的组件库。

共同点是：先把读者带到结果里，再解释实现。

### 2. 让读者在一分钟内看到一次成功

Gum 的 Tutorial 从一个提交信息脚本开始，命令一条条展开；uv 的项目示例包含初始化、添加依赖、运行检查，以及真实输出；这比“本项目包含若干功能”更有说服力。

共同点是：示例不是装饰，而是产品的最短体验路径。

### 3. 语气像维护者在和使用者说话

这些项目会用“Let's build…”, “make it your own”, “Just …, please”这类有判断、有温度的句子。它们不把 README 写成验收清单，也不把内部流程当成产品卖点。

### 4. 安装靠前，但发布和维护不抢第一屏

安装方式通常紧跟在定位和最小示例之后。贡献、开发环境、授权、赞助等内容会放在后半段，或者链接到单独文档。用户打开项目时首先看到的是“我为什么要用”和“怎么马上用起来”。

### 5. 诚实写清边界，反而更可信

uv 用 FAQ 说明稳定性和平台支持；Zed 明确列出还不可用的平台；这类限制说明不会削弱产品，反而让读者知道预期。

### 6. 细节服务于行动，不服务于炫技

成熟 README 会保留能帮助用户运行、判断、排错的细节；不会把所有内部脚本、提交流程、发布命令都塞进产品首页。

## 三、当前项目为什么“没有人味”

当前 README 的能力是完整的，但表达顺序更像内部验收文档：

1. 开头的 “evidence-aware Codex Skill” 是准确术语，却没有先让普通用户感到“这能帮我做什么”。
2. `What it handles` 主要是功能名词列表，缺少一个真实用户从输入到面板的短故事。
3. 有使用命令，但第一屏没有一个可直接感知的面板片段、截图或前后对照。
4. `Development` 和 `Publish to GitHub` 把维护者工作流带进了产品首页；用户并不需要先知道仓库怎么发布。
5. README 里有明显的编码乱码（例如 `鈥?` 一类字符），会直接破坏可信度和“人写的”感觉。
6. “clone、GitHub CLI、dirty worktree、执行策略”等内容属于维护者或自动化代理说明，不属于普通使用者的最短路径。

## 四、我建议的改稿方向

### README 第一屏

改成“产品名 + 一句口语化承诺 + 一个结果示例”：

> Give me a few honest details about yourself, and this Skill turns them into a game-style character panel — stats, skills, quests, gear, and the next unlock.

紧接着放一个极短的输入示例和输出片段，例如：

```text
Use $build-character-panel to turn this self-introduction into a quick panel:
I write lesson materials, keep revising them, and want to finish a reusable template this week.
```

然后展示 6–10 行结果：角色定位、已证实属性、当前任务、未知项和下一步解锁。读者先看到“成品长什么样”，再决定是否继续读。

### README 正文顺序

1. 一句话定位：它为谁解决什么问题。
2. 30 秒示例：最短调用方式与一段输出。
3. 你可以拿它做什么：快速面板、深度访谈、资料转换、更新旧面板。
4. 它如何保持可信：证据状态、未知项、冲突、隐私边界。
5. 安装：只保留用户真正需要的复制步骤。
6. 更多示例和完整规范：链接到 `docs/` 与 `skills/build-character-panel/`。
7. 贡献、开发、发布、许可证：放到末尾或独立维护者文档。

### 语气调整

- 把“Every material claim can be …”改成更像承诺的句子：`If the source does not support a stat, the panel leaves it unknown instead of making one up.`
- 把“Unknown is not zero …”保留，但改成面向用户的提醒：`Unknown is a blank slot to unlock, not a score of zero.`
- 多用 `you / your panel / your next unlock`，少用“system、contract、inventory”这类内部术语。
- 游戏感只负责让信息好读，证据和隐私负责让它可靠；两者在文案中都要出现。

### 文件结构调整

- 从 README 移除 `Publish to GitHub` 整节。
- 若确实要保留发布脚本，放到 `docs/maintainers/github-publishing.md`，标题明确写“维护者文档”。
- 可以增加 `docs/examples/quick-panel.md`，放一份完整、但明确标注为示例的中文或英文面板。
- 清理全仓库 UTF-8 乱码，并在发布前用真实渲染结果复查 README。

## 五、具体改动清单（下一次修改时执行）

- [ ] 重写 README 前 60 行：定位、最短示例、成品片段、安装。
- [ ] 把功能列表改成用户结果列表，并给每项配一个入口句。
- [ ] 增加“为什么不会乱编”的 3 条说明和隐私边界。
- [ ] 移除 README 中面向 Git/CLI/发布自动化的操作说明，迁移到维护者文档。
- [ ] 修复全部中文标点和编码乱码。
- [ ] 补一个真实可读的示例面板，并标明哪些字段是 `stated`、`inferred`、`unknown`。
- [ ] 改稿后重新运行测试、Skill 校验，并从 GitHub 远端重新读取 README 验证实际显示内容。

## 结论

这个项目不缺功能，缺的是“先让人看见自己会得到什么”的入口。下一版应该像 Gum、uv、shadcn/ui 那样，先给一个可想象、可运行、可复用的瞬间；把证据和隐私作为产品可信度；把发布脚本等内部流程放到幕后。这样才是一个开发者在发布产品，而不是一份自动生成的工程清单。

