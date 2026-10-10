# ahebbx/skills

个人 AI 技能（Agent Skills）仓库，把日常真实在用的流程做成可安装的技能。每个技能就是一份 `SKILL.md`，**Codex、Cursor、Claude Code 等支持 Agent Skills 的 AI Agent 都能装**：

| 技能 | 一句话 |
|------|--------|
| [今天吃什么 (what-to-eat)](#今天吃什么-what-to-eat) | 终结每天"吃什么"的纠结，越用越懂你 |
| [视频表达教练 (video-coach)](#视频表达教练-video-coach) | 每天录视频练表达，AI 本地转写+看画面，双轨点评你的口播 |
| [每日英语练习 (daily-english-practice)](#每日英语练习-daily-english-practice) | 每天 15 分钟：当天新闻练阅读、真实场景练写作，弱点靶向复习 |
| [健康方案 (health-plan)](#健康方案-health-plan) | 运动、饮食、睡眠、压力四维方案，打卡记录、定期复盘 |

## 安装

一行命令，自动识别你装了哪些 AI Agent（Codex / Cursor / Claude Code …）并装进去：

```bash
npx skills add ahebbx/skills
```

装完重开会话即可。只想装某个技能或某个 Agent：

```bash
npx skills add ahebbx/skills -s what-to-eat
npx skills add ahebbx/skills -a codex -a cursor
```

**没有命令行？** 打开对应的 `SKILL.md`，把内容复制给任意 AI 当提示词也能用（网页聊天没有文件系统，记录类功能会跳过）。

### 其他安装方式

<details>
<summary>Claude Code 插件市场</summary>

```
/plugin marketplace add ahebbx/skills
/plugin install what-to-eat@ahebbx-skills
/plugin install video-coach@ahebbx-skills
/plugin install daily-english-practice@ahebbx-skills
/plugin install health-plan@ahebbx-skills
```

</details>

<details>
<summary>Claude 桌面版 / 网页版（.skill 安装包）</summary>

下载对应的 `.skill` 文件（[what-to-eat.skill](./what-to-eat.skill) / [video-coach.skill](./video-coach.skill) / [daily-english-practice.skill](./daily-english-practice.skill) / [health-plan.skill](./health-plan.skill)），发到对话里，点卡片上的 **Save skill** 即可。

</details>

---

## 今天吃什么 (what-to-eat)

综合当天天气、你最近吃过什么、营养均衡和你的状态，直接告诉你这顿吃什么——1 个首选 + 2 个备选，每个都有贴合当天的理由，还会维护一份饮食日志，越用越懂你。

### 使用

安装后直接问：

- "今天中午吃什么？"
- "晚上吃啥，累了不想做饭"
- "早餐推荐一下，包子吃腻了"

第一次会问你城市和状态；之后它会查当天天气、避开你最近 3 天吃过的、照顾营养均衡。吃完说一声吃了什么，它会记进 `~/.what-to-eat/饮食记录.md`（家目录统一路径，不管在哪个 Agent、哪个项目里问都是同一份记录）——记录越多，推荐越准。告诉它忌口（"我不吃香菜"）会永久记住。

---

## 视频表达教练 (video-coach)

每天录一条视频练表达/口播，录完让 AI 当教练。所有处理都在本地完成（视频不上传任何地方）：whisper 转写出带时间戳的字幕，每 20 秒抽一帧看画面，然后**双轨点评**——

- **内容轨**：结构（10 秒入题？总-分-总？）、冗余、口头禅逐词计数（不是估计，是真数）、逻辑断层
- **画面轨**：眼神方向、光线、构图、表情、背景
- **交叉印证**：句子崩塌的时间点，往往正对着眼神下垂的那一帧——两轨对上号，你才知道根因是"没想清"而不是"不会说"

每次点评**只给一个改进点**（单点突破胜过面面俱到），并维护练习日志，逐天对比让你看见哪里在变好、哪里在原地踏步。

### 使用

安装后录完视频直接说：

- "看下今天的视频"
- "点评一下这条练习视频"

用 macOS 自带的 QuickTime 录（文件 → 新建影片录制）就行，录完忘了按 ⌘S 也没关系——脚本会自动从 QuickTime 未存储的录制里把视频抢救出来。

**依赖**（macOS）：`brew install ffmpeg whisper-cpp`，外加一个 whisper 模型（缺什么脚本会直接给出安装命令）。

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

技能本身不含调度：把「使用 daily-english-practice skill 开始今日练习」这句提示词，交给你所用 Agent 的定时任务功能即可（例如 Claude 的 Scheduled Task、Claude Code 的 `/loop`）。

---

## 健康方案 (health-plan)

根据你的目标（减脂 / 增肌 / 改善体能 / 改善睡眠）、可用时间和场地，制定运动、饮食、睡眠、压力管理四维个性化方案；之后每天打卡记录进度，到检查点自动复盘——执行率低就简化，完成得好就小步加量（每周增量不超过 10%）。

### 使用

安装后直接说：

- "帮我做个健康计划"
- "今天走了 40 分钟，做了拉伸，精力 6 分"
- "今天该练什么？"

方案和进度固定存在 `~/.health-plan/`（`plan.md` 当前方案、`progress.md` 进度日志），任何 Agent 里触发都读写同一份数据。涉及慢性病、伤痛、孕期等情况会提醒先咨询医生。

---

## 结构

```
├── .claude-plugin/
│   └── marketplace.json          # 插件市场清单（ahebbx-skills）
├── plugins/
│   ├── what-to-eat/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/what-to-eat/
│   │       ├── SKILL.md          # 主流程
│   │       └── references/       # 时令食材、菜品库
│   ├── video-coach/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/video-coach/
│   │       ├── SKILL.md          # 双轨点评流程
│   │       └── scripts/
│   │           └── prepare.sh    # 定位视频→抢救未存储→转写→抽帧
│   ├── daily-english-practice/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/daily-english-practice/
│   │       └── SKILL.md          # 课程主流程
│   └── health-plan/
│       ├── .claude-plugin/plugin.json
│       └── skills/health-plan/
│           └── SKILL.md          # 方案制定、打卡、复盘
├── what-to-eat.skill             # .skill 一键安装包
├── video-coach.skill
├── daily-english-practice.skill
└── health-plan.skill
```

## License

MIT
