# daily-english-practice 技能移植设计

- 日期: 2026-07-28
- 状态: 已批准（用户确认方案 A + 完整发布范围）

## 背景

桌面版 Claude 有一个 Scheduled Task `/Users/shuifu/Claude/Scheduled/daily-english-practice/SKILL.md`：给 Lucas（中文母语，B1-B2）做每日英语读写练习，目标是读懂英文美国新闻 + 用英文和 AI 工具工作沟通。任务提示词内嵌 LEARNER RECORD（已用话题、难度校准、弱点清单等），靠桌面版 scheduled-tasks update tool 维护。

本设计把它移植为 ahebbx/skills 仓库的第三个技能，与 what-to-eat、video-coach 完全对齐。

## 已确认的决策

1. **完全通用化**：SKILL.md 不写死个人信息；首次使用时询问姓名/水平/目标并建档。公开仓库不含任何个人数据。
2. **方案 A（复刻 what-to-eat 模式）**：学习者记录存家目录固定路径 `~/.daily-english-practice/学习记录.md`，技能每次开始读、结束更新；现有 LEARNER RECORD 作为种子内容迁入该文件（本地文件，不进仓库）。
3. **完整发布**：插件本体 + marketplace.json + README + .skill 安装包 + git 提交。

## 交付物

### 1. 插件本体

```
plugins/daily-english-practice/
├── .claude-plugin/plugin.json
└── skills/daily-english-practice/
    └── SKILL.md          # 单文件主流程，不拆 references（源提示词为 20 行高内聚流程，拆分属过度设计）
```

`plugin.json`：

```json
{
  "name": "daily-english-practice",
  "description": "每日英语读写练习：当天真实新闻改编阅读+实用写作任务+弱点靶向复习，维护学习记录越练越准",
  "version": "1.0.0",
  "author": { "name": "ahebbx" }
}
```

### 2. SKILL.md 改编

frontmatter：

```yaml
---
name: daily-english-practice
description: 每日英语读写能力练习。当用户说"每日英语""今日英语练习""英语练习""开始今天的英语""练英语"或"daily English practice"，或想做英语读写训练时使用。用当天真实新闻做分级阅读+实用写作，针对个人弱点靶向复习，并维护学习记录越练越懂你。
---
```

正文结构：

1. **读取记录**：用 bash `date` 拿当前日期；读 `~/.daily-english-practice/学习记录.md`。
   - 不存在 → 首次建档：问姓名、水平（默认参考 B1-B2 中级）、学习目标（默认示例：读懂英文新闻、用英文和 AI 工具沟通），`mkdir -p ~/.daily-english-practice` 并创建文件。
   - 存在 → 通读，重点：水平与难度校准、进阶计划、弱点清单（最新几条）、已用新闻话题。
2. **课程五步**（原样保留桌面版教学法）：
   - 阅读：web search 找当天/昨天的真实美国新闻一篇，改写成学习者水平 150–250 词短文；5–8 个关键词汇（英文释义+中文翻译）；3 道英文理解题。
   - 写作：一个短任务，(a) 2–3 句自己话总结短文 与 (b) 职场实用任务（给 AI 写英文提示词/消息，含真实场景）交替变化。
   - 复习：从记录编织 1–2 个弱点项进课程（词汇表收录、理解题/写作场景强制使用、或快速复习题），标注为靶向复习。
   - 收尾：用中文邀请在本会话作答；作答后温和但彻底地批改，中文讲解语法和用词问题，给更地道的替代说法，并告知今天难度偏易/合适/偏难。
   - 维护：参与过的会话结束时更新记录文件——新暴露的问题带日期追加，掌握了的移除或标记，保持 ~20 行内、最新在前。
3. **风格规则**（保留）：指令和讲解用中文，练习内容全英文；15 分钟内可完成；话题和词汇逐日变化；不重复前一天的新闻。
4. **降级**：web search 不可用时，选用记录里没出现过的常识性时事话题，或请学习者指定话题，不硬失败。

### 3. 学习者记录文件

`~/.daily-english-practice/学习记录.md`（本地家目录，不进仓库）：

```markdown
# 英语学习记录

## 基本信息
- 姓名: Lucas
- 水平: B1-B2（中级）
- 目标: 读懂英文美国新闻；用英文和 AI 工具工作沟通（写提示词、指令、消息）
- 备注: 2026-07-28 从桌面版定时任务迁移建档

## 练习记录
<种子 = 桌面版 SKILL.md 中 LEARNER RECORD 全部内容，原样迁入：已用话题、难度校准、进阶计划、有效框架、弱点清单（倒序）、正向反馈>
```

首次使用的其他用户：只建 基本信息 + 空的 练习记录 骨架。

### 4. marketplace.json

追加第三条：

```json
{
  "name": "daily-english-practice",
  "source": "./plugins/daily-english-practice",
  "description": "每日英语读写练习：当天新闻改编阅读+实用写作+弱点复习，学习记录追踪进步"
}
```

### 5. README.md

- 表格加一行（技能名 + 一句话简介）
- 新增 `## 每日英语练习 (daily-english-practice)` 小节：简介 + 使用（"今日英语练习"等触发说法）+ 首次使用说明 + 调度接法（桌面版 Scheduled Tasks 提示词写"使用 daily-english-practice skill 开始今日练习"；Claude Code 用 /loop 或 cron）+ 记录文件路径说明
- 结构树加入新插件目录

### 6. .skill 安装包

```bash
cd plugins/daily-english-practice/skills
zip -0 -r ../../../daily-english-practice.skill daily-english-practice/
```

（`-0` store 模式，与现有两个 .skill 包一致。）

### 7. git

- 本 spec 单独一个 commit（`docs: add daily-english-practice port design spec`）
- 实现完成后一个 commit：`feat: add daily-english-practice skill (每日英语练习) v1.0.0`

## 数据流

```
触发（"今日英语练习" / 调度器一句话）
  → date 拿日期 → 读 ~/.daily-english-practice/学习记录.md（缺失则建档）
  → web search 取当日新闻 → 出课（阅读+词汇+理解题+写作任务+靶向复习）
  → 学习者作答 → 批改+讲解+难度反馈
  → 更新学习记录.md
```

调度配置不进仓库，只在 README 说明接法。

## 错误处理

| 情况 | 处理 |
|---|---|
| 记录文件不存在 | 走首次建档流程 |
| 记录文件损坏/读不出 | 不清空，提示用户并先备份再重建 |
| web search 不可用 | 常识性时事话题或用户指定话题降级 |

## 验收

与仓库现状一致，无自动化测试：

1. 模拟首次建档：把已种子的记录文件临时改名挪走 → 跑流程应问出姓名/水平/目标并正确建档 → 删除测试建的文件、恢复种子文件（全程不丢种子数据）
2. 完整跑一节课：课程结构齐全（阅读/词汇/理解题/写作/复习标注），结束后记录文件被正确更新
3. `plugin.json`、`marketplace.json` 通过 JSON 校验
4. `.skill` zip 内容核对（含 `daily-english-practice/SKILL.md`，结构与现有包一致）

## 不在范围

- 任何调度配置本身（cron/launchd/桌面版 Scheduled Tasks 的创建与修改）
- 桌面版原定时任务的去留；其提示词替换文本在实现结束后提供给用户手动操作
- 教学法的改动（源提示词的教学设计原样保留）
