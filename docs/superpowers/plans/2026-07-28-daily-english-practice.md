# daily-english-practice 技能移植实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把桌面版定时任务 daily-english-practice 移植为 ahebbx/skills 仓库的第三个技能（插件本体 + 市场清单 + README + .skill 安装包 + 本地学习者记录种子）。

**Architecture:** 复刻 what-to-eat 模式：SKILL.md 通用（首次使用问姓名/水平/目标建档），学习者记录存家目录固定路径 `~/.daily-english-practice/学习记录.md`，现有 LEARNER RECORD 原样种子迁入。调度不进仓库，README 说明各平台接法。

**Tech Stack:** Claude Agent Skill（SKILL.md + YAML frontmatter）、Claude Code 插件市场（plugin.json / marketplace.json）、zip（.skill 安装包）。

**Spec:** `docs/superpowers/specs/2026-07-28-daily-english-practice-design.md`（已批准）

## Global Constraints

- 仓库根：`/Users/shuifu/Documents/project/skills`，所有相对路径以此为准
- 插件版本 `1.0.0`，author `{ "name": "ahebbx" }`
- 学习者记录路径固定为 `~/.daily-english-practice/学习记录.md`（家目录，**不进仓库、不提交**）
- SKILL.md 单文件，不拆 references/
- .skill 打包用 store 模式（`zip -0 -r`），与现有两个包一致
- 教学法原样保留：阅读 150–250 词 + 5–8 词汇 + 3 理解题；写作 (a)总结/(b)AI提示词 交替；1–2 个弱点靶向复习；一节课约 15 分钟；连续两天不重复新闻
- 实现为**单一 commit**：`feat: add daily-english-practice skill (每日英语练习) v1.0.0`（各 Task 不单独提交）

---

### Task 1: 插件本体（plugin.json + SKILL.md）

**Files:**
- Create: `plugins/daily-english-practice/.claude-plugin/plugin.json`
- Create: `plugins/daily-english-practice/skills/daily-english-practice/SKILL.md`

**Interfaces:**
- Consumes: 无
- Produces: 插件目录结构；Task 4 的 zip 打包读取 `plugins/daily-english-practice/skills/daily-english-practice/`

- [ ] **Step 1: 创建目录**

```bash
mkdir -p /Users/shuifu/Documents/project/skills/plugins/daily-english-practice/.claude-plugin
mkdir -p /Users/shuifu/Documents/project/skills/plugins/daily-english-practice/skills/daily-english-practice
```

- [ ] **Step 2: 写 plugin.json**

文件 `plugins/daily-english-practice/.claude-plugin/plugin.json`：

```json
{
  "name": "daily-english-practice",
  "description": "每日英语读写练习：当天真实新闻改编阅读+实用写作任务+弱点靶向复习，维护学习记录越练越准",
  "version": "1.0.0",
  "author": { "name": "ahebbx" }
}
```

- [ ] **Step 3: 校验 JSON**

Run: `python3 -m json.tool /Users/shuifu/Documents/project/skills/plugins/daily-english-practice/.claude-plugin/plugin.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 4: 写 SKILL.md**

文件 `plugins/daily-english-practice/skills/daily-english-practice/SKILL.md`，完整内容：

````markdown
---
name: daily-english-practice
description: 每日英语读写能力练习。当用户说"每日英语""今日英语练习""英语练习""开始今天的英语""练英语"或"daily English practice"，或想做英语读写训练时使用。用当天真实新闻做分级阅读+实用写作，针对个人弱点靶向复习，并维护学习记录越练越懂你。
---

# 每日英语练习

为学习者做每日英语读写训练。核心思路：先读学习记录了解他，再用当天真实新闻出一节约 15 分钟的课，作答后批改并把新发现记回记录——记录越多，课越准。

## 工作流程

### 1. 拿日期、读学习记录

用 bash `date` 拿当前日期（注意用户时区）。读取 **`~/.daily-english-practice/学习记录.md`**（家目录统一路径——不管在哪个工具、哪个项目里触发，读写的都是同一份记录）。

- **找到了**：通读一遍。重点：英语水平与难度校准、进阶计划、弱点清单（最新几条优先）、已用新闻话题（今天不能重复）。
- **没找到**：首次使用。用 AskUserQuestion 一次问清：姓名、英语水平（默认参考 B1-B2 中级）、学习目标（默认示例：读懂英文新闻、用英文和 AI 工具工作沟通）。然后 `mkdir -p ~/.daily-english-practice` 并按文末格式建档（练习记录先留空骨架）。
- **文件损坏/读不出**：不要清空。提示用户，先把原文件复制为 `学习记录.md.bak` 再重建。
- 无文件系统的环境：跳过读写，直接靠对话内信息上课。

### 2. 阅读（Reading）

用 web search 找一篇当天或昨天的真实美国新闻，话题不得与记录中的已用话题重复。以记录里的水平和难度校准为基准（并根据他当次会话的表现微调），改写成该水平的英文短文，150–250 词。文后给：

- 5–8 个关键词汇/短语：每个配一句简短英文释义 + 中文翻译
- 3 道英文理解题

若记录中有进阶计划（如每周一次"原文挑战"：附一小段未改写的真实原文），按计划执行并标注。

web search 不可用：选用记录里没出现过的常识性时事话题，或请学习者指定话题，不硬失败。

### 3. 写作（Writing）

给 ONE 个短写作任务，紧贴他的学习目标，逐日交替变化：

- (a) 用 2–3 句自己的话总结今天的短文（必须 own words，严防照抄原句）；或
- (b) 职场实用任务：给一个真实场景，让他给 AI 助手写英文提示词/消息（如请 AI 起草邮件、分析数据、排查问题）。

### 4. 复习（Review）

从学习记录的弱点清单里挑 1–2 项编织进今天的课：收进词汇表、设计一道强制用到它的理解题或写作场景、或加一道快速复习题。标注为靶向复习，让他知道这是针对弱点的。

### 5. 收尾与批改

用中文邀请他在本会话作答。若他作答：温和但彻底地批改英文，用中文讲解语法和用词问题，给出更地道/自然的替代说法，回答他的疑问，并告诉他今天的难度偏易/合适/偏难。

### 6. 维护记录

他参与过的会话结束时，更新 `~/.daily-english-practice/学习记录.md`：

- 新暴露的问题带日期追加进弱点清单
- 持续做对的项移除或标记已掌握
- 已用话题补充今天的新闻主题
- 难度校准和进阶计划按他的反馈更新

弱点清单最新在前；练习记录整体保持紧凑（约 20 行内，掌握了就删，给新发现腾位置）。

## 风格规则

- 指令和讲解用中文；所有练习内容用英文
- 一节课约 15 分钟可完成，保持紧凑
- 话题和词汇逐日变化；连续两天不用同一新闻

## 学习记录.md 格式

```markdown
# 英语学习记录

## 基本信息
- 姓名: （首次使用时填写）
- 水平: （如 B1-B2 中级）
- 目标: （如 读懂英文美国新闻；用英文和 AI 工具工作沟通）

## 练习记录
（最新在前：已用新闻话题、难度校准、进阶计划、有效框架、弱点清单、正向反馈）
```
````

- [ ] **Step 5: 验证 SKILL.md 结构**

Run:
```bash
S=/Users/shuifu/Documents/project/skills/plugins/daily-english-practice/skills/daily-english-practice/SKILL.md
grep -c '^### ' "$S"
grep -c '150–250\|学习记录.md\|AskUserQuestion\|靶向复习\|原文挑战' "$S"
head -4 "$S"
```
Expected: 第一个数 `6`（六个工作流小节）；第二个数 ≥5；head 输出以 `---` 起、含 `name: daily-english-practice` 和 `description:`

（本 Task 不提交，统一在 Task 4 提交。）

---

### Task 2: 学习者记录种子文件（本地，不进仓库）

**Files:**
- Create: `/Users/shuifu/.daily-english-practice/学习记录.md`

**Interfaces:**
- Consumes: 桌面版 `/Users/shuifu/Claude/Scheduled/daily-english-practice/SKILL.md` 的 LEARNER RECORD（内容已完整抄录如下）
- Produces: skill 首次运行时读取的记录文件；Task 4 验收时 grep 校验

- [ ] **Step 1: 创建目录**

```bash
mkdir -p /Users/shuifu/.daily-english-practice
```

- [ ] **Step 2: 写种子文件**

文件 `/Users/shuifu/.daily-english-practice/学习记录.md`，完整内容（LEARNER RECORD 原样迁入 练习记录 区）：

```markdown
# 英语学习记录

## 基本信息
- 姓名: Lucas
- 水平: B1-B2（中级）
- 目标: 读懂英文美国新闻；用英文和 AI 工具工作沟通（写提示词、指令、消息）
- 备注: 2026-07-28 从桌面版定时任务迁移建档

## 练习记录
Recent news topics used (do not repeat): 07-19 World Cup final/halftime show; 07-18 X open-sourcing its codebase.
Difficulty calibration: 07-19 level right — comprehension fully correct (new words flagged were only proper nouns + sports terms); production error-rich but all drills landed. Keep B1-B2 + one B2+ structure. Production is priority; own-words improving but first sentences still near-verbatim — keep requiring own words.
Progression plan (set 07-19, he asked about timeline): starting ~07-26, include one short UNADAPTED excerpt from the real source article each week (labeled original challenge) alongside the adapted passage; grow the share of authentic text over time.
Frameworks that work: SVO main/modifier (07-18) — on 07-19 he used it to parse an appositive correctly (previous weakness, now improved). Also taught refer to / modify / describe metalanguage.

Weak points (most recent first):
- 07-19 HIGH NEW: comma splice x2 in one session (Chinese-transfer). Drill: fix run-on sentences.
- 07-19 HIGH update on S-V agreement: recognition drill PASSED but x2 errors in free writing ("there is two reason", "My manager need") — shift to self-check-own-writing drills; "there is/are + plural" is his trap variant.
- 07-19 NEW: drops -ed in be + past participle x2 ("is play", "is not limit"). Drill passive forms.
- 07-19 NEW: drops plural -s x2 ("two reason", "the top thing client liked").
- 07-19: too vs so ("too many stars" intended positively).
- 07-19: chunk-stitching AGAIN (copied "that has never happened before" with no head noun; 3rd occurrence) — keep HIGH; rule: before reusing a phrase, check the new sentence has a hook for it.
- 07-19: preposition + time word — erred again ("on tomorrow morning") but found "in next Tuesday" in a drill same-day. Taught deadline "by". Retest cold next session.
- 07-19 RETEST FAILED then re-taught: AI-prompt 4-part structure — again omitted requirements + format/length; after re-teach wrote "Format is not limit" (missed the WHY: always cap length). Retest task (b) within 2-3 sessions.
- 07-19 minor: Chinese punctuation in English text; large numbers need commas (82,500).
- 07-18 minor not retested: capitalization of names; standalone "Because..." fragments.
- 07-17 not retested: advice/advise, analysis/analyze, serve/server; brief/briefly; quarter vs season; modifier placement; register (no casual abbreviations).
Positive 07-19: appositive parsing OK; S-V recognition drill OK; same-day error transfer OK; ended with a usable work prompt mostly self-written.
```

- [ ] **Step 3: 验证种子内容完整**

Run:
```bash
R=/Users/shuifu/.daily-english-practice/学习记录.md
grep -c '^- 07-1' "$R"
grep -c 'Lucas\|B1-B2\|comma splice\|Recent news topics\|Progression plan\|Positive 07-19' "$R"
```
Expected: 第一个数 `11`（11 条弱点清单条目）；第二个数 `7`

（本文件在家目录，永不 git add。）

---

### Task 3: marketplace.json + README.md

**Files:**
- Modify: `.claude-plugin/marketplace.json`（追加第三条插件）
- Modify: `README.md`（表格行、安装说明、新技能小节、结构树，共 4 处）

**Interfaces:**
- Consumes: Task 1 的插件目录名 `daily-english-practice`
- Produces: Task 4 提交时一起入库

- [ ] **Step 1: marketplace.json 追加插件条目**

将 `.claude-plugin/marketplace.json` 整体替换为：

```json
{
  "name": "ahebbx-skills",
  "owner": { "name": "ahebbx" },
  "plugins": [
    {
      "name": "what-to-eat",
      "source": "./plugins/what-to-eat",
      "description": "「今天吃什么」决策助手：综合天气时令、饮食记录、营养均衡，直接告诉你这顿吃什么"
    },
    {
      "name": "video-coach",
      "source": "./plugins/video-coach",
      "description": "视频表达教练：本地转写练习视频+抽帧看画面，双轨点评，每天一个改进点，练习日志追踪进步"
    },
    {
      "name": "daily-english-practice",
      "source": "./plugins/daily-english-practice",
      "description": "每日英语读写练习：当天新闻改编阅读+实用写作+弱点复习，学习记录追踪进步"
    }
  ]
}
```

- [ ] **Step 2: 校验 JSON**

Run: `python3 -m json.tool /Users/shuifu/Documents/project/skills/.claude-plugin/marketplace.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 3: README 表格加一行**

Edit `README.md`，old_string：

```
| [视频表达教练 (video-coach)](#视频表达教练-video-coach) | 每天录视频练表达，AI 本地转写+看画面，双轨点评你的口播 |
```

new_string：

```
| [视频表达教练 (video-coach)](#视频表达教练-video-coach) | 每天录视频练表达，AI 本地转写+看画面，双轨点评你的口播 |
| [每日英语练习 (daily-english-practice)](#每日英语练习-daily-english-practice) | 每天 15 分钟：当天新闻练阅读、真实场景练写作，弱点靶向复习 |
```

- [ ] **Step 4: README 安装说明加第三技能**

Edit `README.md`，old_string：

```
/plugin install what-to-eat@ahebbx-skills
/plugin install video-coach@ahebbx-skills
```

new_string：

```
/plugin install what-to-eat@ahebbx-skills
/plugin install video-coach@ahebbx-skills
/plugin install daily-english-practice@ahebbx-skills
```

再改桌面版下载行，old_string：

```
下载对应的 `.skill` 文件（[what-to-eat.skill](./what-to-eat.skill) / [video-coach.skill](./video-coach.skill)），发到 Claude 对话里，点卡片上的 **Save skill** 即可。
```

new_string：

```
下载对应的 `.skill` 文件（[what-to-eat.skill](./what-to-eat.skill) / [video-coach.skill](./video-coach.skill) / [daily-english-practice.skill](./daily-english-practice.skill)），发到 Claude 对话里，点卡片上的 **Save skill** 即可。
```

- [ ] **Step 5: README 插入新技能小节**

Edit `README.md`，old_string：

```
**配置**（可选环境变量）：`VIDEO_COACH_DIR` 视频目录（默认 `~/Movies/录视频练习`）、`VIDEO_COACH_MODEL` 模型路径、`VIDEO_COACH_LANG` 转写语言（默认 zh）、`VIDEO_COACH_LOG` 练习日志路径。

---

## 结构
```

new_string：

```
**配置**（可选环境变量）：`VIDEO_COACH_DIR` 视频目录（默认 `~/Movies/录视频练习`）、`VIDEO_COACH_MODEL` 模型路径、`VIDEO_COACH_LANG` 转写语言（默认 zh）、`VIDEO_COACH_LOG` 练习日志路径。

---

## 每日英语练习 (daily-english-practice)

每天 15 分钟的英语读写私教：用当天真实的美国新闻做分级阅读（关键词汇 + 理解题），写作任务在「总结短文」和「给 AI 写英文提示词」之间交替，再从你的历史弱点里挑 1–2 个编织进当天的课做靶向复习。作答后温和批改、中文讲解，并维护一份学习记录——练得越多，课越贴你的水平。

### 使用

安装后直接说：

- "今日英语练习"
- "开始今天的英语"
- "daily English practice"

第一次会问你的姓名、英语水平和学习目标；之后每次开始先读 `~/.daily-english-practice/学习记录.md`（家目录统一路径，任何工具里触发都是同一份记录），结束把新发现的弱点、难度校准和当天话题记回去。

### 定时自动练

技能本身不含调度，接到各平台的定时能力上即可：

- **Claude 桌面版 / claude.ai**：建一个 Scheduled Task，提示词写「使用 daily-english-practice skill 开始今日练习」
- **Claude Code**：用 `/loop` 或定时任务跑同样的提示词

---

## 结构
```

- [ ] **Step 6: README 结构树更新**

Edit `README.md`，old_string：

```
│   └── video-coach/
│       ├── .claude-plugin/plugin.json
│       └── skills/video-coach/
│           ├── SKILL.md          # 双轨点评流程
│           └── scripts/
│               └── prepare.sh    # 定位视频→抢救未存储→转写→抽帧
├── what-to-eat.skill             # Claude 桌面版一键安装包
└── video-coach.skill
```

new_string：

```
│   ├── video-coach/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/video-coach/
│   │       ├── SKILL.md          # 双轨点评流程
│   │       └── scripts/
│   │           └── prepare.sh    # 定位视频→抢救未存储→转写→抽帧
│   └── daily-english-practice/
│       ├── .claude-plugin/plugin.json
│       └── skills/daily-english-practice/
│           └── SKILL.md          # 课程主流程
├── what-to-eat.skill             # Claude 桌面版一键安装包
├── video-coach.skill
└── daily-english-practice.skill
```

- [ ] **Step 7: 验证 README 四处修改**

Run:
```bash
cd /Users/shuifu/Documents/project/skills
grep -c 'daily-english-practice' README.md
```
Expected: `9`（表格行、安装、下载行、小节标题、记录路径说明、调度提示词各 1 行 + 结构树 3 行）

---

### Task 4: .skill 打包 + 验收 + 单一 commit

**Files:**
- Create: `daily-english-practice.skill`（zip，入库）

**Interfaces:**
- Consumes: Task 1 的 `plugins/daily-english-practice/skills/daily-english-practice/`、Task 3 的全部修改
- Produces: 最终 commit `feat: add daily-english-practice skill (每日英语练习) v1.0.0`

- [ ] **Step 1: 打包 .skill（store 模式，排除 .DS_Store）**

```bash
cd /Users/shuifu/Documents/project/skills/plugins/daily-english-practice/skills
zip -0 -r ../../../daily-english-practice.skill daily-english-practice/ -x "*.DS_Store"
```

- [ ] **Step 2: 核对 zip 内容**

Run: `unzip -l /Users/shuifu/Documents/project/skills/daily-english-practice.skill`
Expected: 含 `daily-english-practice/` 目录条目和 `daily-english-practice/SKILL.md`，共 2–3 个条目，无 .DS_Store

- [ ] **Step 3: 全量验收检查**

Run:
```bash
cd /Users/shuifu/Documents/project/skills
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo marketplace-OK
python3 -m json.tool plugins/daily-english-practice/.claude-plugin/plugin.json > /dev/null && echo plugin-OK
test -f plugins/daily-english-practice/skills/daily-english-practice/SKILL.md && echo skillmd-OK
test -f daily-english-practice.skill && echo pkg-OK
test -f /Users/shuifu/.daily-english-practice/学习记录.md && echo seed-OK
git status --short
```
Expected: 五行全 OK；git status 列出：新插件目录、`daily-english-practice.skill`、修改的 `marketplace.json` 和 `README.md`、（以及已提交的 spec/plan 文档不出现）。**不应出现** `.daily-english-practice/`（在家目录不在仓库）

- [ ] **Step 4: 单一 commit**

```bash
cd /Users/shuifu/Documents/project/skills
git add plugins/daily-english-practice daily-english-practice.skill .claude-plugin/marketplace.json README.md
git commit -m "feat: add daily-english-practice skill (每日英语练习) v1.0.0

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

- [ ] **Step 5: 交付手动验收说明**

实现结束后向用户交付两条手动操作：

1. **冒烟测试（读档路径）**：新会话里说「今日英语练习」——应直接读到 Lucas 的档案出课（不再问姓名/水平），且今天的新闻话题不是 World Cup / X open-sourcing。课结束后检查 `~/.daily-english-practice/学习记录.md` 已追加今天的话题条目。
2. **首次建档路径**（可选，验证 spec 验收 #1）：
   ```bash
   mv ~/.daily-english-practice/学习记录.md ~/.daily-english-practice/学习记录.md.keep
   ```
   新会话说「今日英语练习」——应走首次建档、问姓名/水平/目标并新建文件。然后删掉新建的测试文件、恢复种子：
   ```bash
   rm ~/.daily-english-practice/学习记录.md
   mv ~/.daily-english-practice/学习记录.md.keep ~/.daily-english-practice/学习记录.md
   ```
3. **桌面版定时任务**（可选）：把原 Scheduled Task 的提示词替换为「使用 daily-english-practice skill 开始今日练习」，或直接停用——否则桌面版继续维护旧提示词里的 LEARNER RECORD，两份记录会分叉。
