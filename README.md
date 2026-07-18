# ahebbx/skills

个人 AI 技能（Agent Skills）仓库，把日常真实在用的流程做成可安装的技能：

| 技能 | 一句话 |
|------|--------|
| [今天吃什么 (what-to-eat)](#今天吃什么-what-to-eat) | 终结每天"吃什么"的纠结，越用越懂你 |
| [视频表达教练 (video-coach)](#视频表达教练-video-coach) | 每天录视频练表达，AI 本地转写+看画面，双轨点评你的口播 |

## 安装

### Claude Code / Codex / Cursor 等（一行命令）

```bash
npx skills add ahebbx/skills
```

装完重开会话即可。也可以只装到指定工具：

```bash
npx skills add ahebbx/skills -a claude-code -a codex
```

### Claude Code 插件市场

```
/plugin marketplace add ahebbx/skills
/plugin install what-to-eat@ahebbx-skills
/plugin install video-coach@ahebbx-skills
```

### Claude 桌面版 / claude.ai

下载对应的 `.skill` 文件（[what-to-eat.skill](./what-to-eat.skill) / [video-coach.skill](./video-coach.skill)），发到 Claude 对话里，点卡片上的 **Save skill** 即可。

---

## 今天吃什么 (what-to-eat)

综合当天天气、你最近吃过什么、营养均衡和你的状态，直接告诉你这顿吃什么——1 个首选 + 2 个备选，每个都有贴合当天的理由，还会维护一份饮食日志，越用越懂你。

### 使用

安装后直接问：

- "今天中午吃什么？"
- "晚上吃啥，累了不想做饭"
- "早餐推荐一下，包子吃腻了"

第一次会问你城市和状态；之后它会查当天天气、避开你最近 3 天吃过的、照顾营养均衡。吃完说一声吃了什么，它会记进 `~/.what-to-eat/饮食记录.md`（家目录统一路径，Claude Code / Codex 等工具、任何项目里问都是同一份记录）——记录越多，推荐越准。告诉它忌口（"我不吃香菜"）会永久记住。

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
│   └── video-coach/
│       ├── .claude-plugin/plugin.json
│       └── skills/video-coach/
│           ├── SKILL.md          # 双轨点评流程
│           └── scripts/
│               └── prepare.sh    # 定位视频→抢救未存储→转写→抽帧
├── what-to-eat.skill             # Claude 桌面版一键安装包
└── video-coach.skill
```

## License

MIT
