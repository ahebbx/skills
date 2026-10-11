# ahebbx/skills

个人 AI 技能（Agent Skills）仓库，把日常真实在用的流程做成可安装的技能。每个技能就是一份 `SKILL.md`，**Codex、Cursor、Claude Code 等支持 Agent Skills 的 AI Agent 都能装，macOS / Windows / Linux 通用**：

| 技能 | 一句话 |
|------|--------|
| [今天吃什么 (what-to-eat)](#今天吃什么-what-to-eat) | 终结每天"吃什么"的纠结，越用越懂你 |
| [视频表达教练 (video-coach)](#视频表达教练-video-coach) | 每天录视频练表达，AI 本地转写+看画面，双轨点评你的口播 |
| [每日英语练习 (daily-english-practice)](#每日英语练习-daily-english-practice) | 每天 15 分钟：当天新闻练阅读、真实场景练写作，弱点靶向复习 |
| [健康方案 (health-plan)](#健康方案-health-plan) | 运动、饮食、睡眠、压力四维方案，打卡记录、定期复盘 |

## 使用教程

macOS、Windows、Linux 都能用，三步装好。

### 第 1 步：装 Node.js（只需一次）

安装命令要用到 Node.js 自带的 `npx`。先打开终端检查一下，能显示版本号（如 `v22.x`）就跳过这一步：

```bash
node -v
```

| 系统 | 打开终端 | 安装 Node.js |
|------|----------|--------------|
| macOS | 启动台搜「终端」 | `brew install node`，或到 [nodejs.org](https://nodejs.org/zh-cn) 下载安装包 |
| Windows | 开始菜单搜「PowerShell」 | `winget install OpenJS.NodeJS.LTS`，或到 [nodejs.org](https://nodejs.org/zh-cn) 下载安装包；装完**关掉重开** PowerShell |
| Linux | `Ctrl + Alt + T` | 到 [nodejs.org](https://nodejs.org/zh-cn/download) 按发行版装 LTS 版（系统软件源里的版本可能太旧） |

### 第 2 步：安装技能

在终端里运行（三个系统命令一样）：

```bash
npx skills add ahebbx/skills -g
```

它会自动识别你电脑上装了哪些 AI Agent（Codex / Cursor / Claude Code …），按提示确认即可。`-g` 表示装到用户目录，在任何文件夹里都能用；不加的话只装进当前文件夹的项目。

只想装其中一个技能，或只装到某个 Agent：

```bash
npx skills add ahebbx/skills -g -s what-to-eat
npx skills add ahebbx/skills -g -a codex -a cursor
```

> **Windows 报错「无法加载文件 npx.ps1，因为在此系统上禁止运行脚本」？** 把命令里的 `npx` 换成 `npx.cmd` 再运行。

### 第 3 步：重开 Agent，直接说话

关掉 Agent 的当前会话再开一个新的，然后像平时聊天一样说：

```
你：今天中午吃什么？
AI：（查天气、看你最近吃过什么）今天就吃番茄牛腩面——降温了来碗热汤面，
    你前两天都是米饭，换换口味……备选：……
```

每个技能能说什么，见下面各技能的「使用」。没反应的话，在话里点名技能，比如「用 what-to-eat 推荐一下午饭」。

### 更新与卸载

```bash
npx skills update -g          # 更新到最新版
npx skills remove -g          # 选择要卸载的技能
```

### 数据存在哪

记录都是本机的 Markdown 文件，可以直接打开看、手动改，换 Agent 也不会丢：

| 技能 | macOS / Linux | Windows |
|------|---------------|---------|
| 今天吃什么 | `~/.what-to-eat/` | `C:\Users\<用户名>\.what-to-eat\` |
| 每日英语 | `~/.daily-english-practice/` | `C:\Users\<用户名>\.daily-english-practice\` |
| 健康方案 | `~/.health-plan/` | `C:\Users\<用户名>\.health-plan\` |
| 视频教练 | `~/Movies/录视频练习/`（Linux 为 `~/Videos/录视频练习/`） | `C:\Users\<用户名>\Videos\录视频练习\` |

### 其他安装方式

<details>
<summary>没有命令行 / 只用网页版 AI</summary>

打开对应技能的 `SKILL.md`（在 `plugins/<技能名>/skills/<技能名>/` 下），把全部内容复制给任意 AI 当提示词就能用。网页聊天读写不了本地文件，所以「记住你吃过什么」这类记录功能会跳过；视频教练需要本地运行脚本，网页版用不了。

</details>

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

从 [Releases](https://github.com/ahebbx/skills/releases/latest) 下载对应的 `.skill` 文件（[what-to-eat.skill](https://github.com/ahebbx/skills/releases/latest/download/what-to-eat.skill) / [video-coach.skill](https://github.com/ahebbx/skills/releases/latest/download/video-coach.skill) / [daily-english-practice.skill](https://github.com/ahebbx/skills/releases/latest/download/daily-english-practice.skill) / [health-plan.skill](https://github.com/ahebbx/skills/releases/latest/download/health-plan.skill)），发到对话里，点卡片上的 **Save skill** 即可。

</details>

<details>
<summary>Codex 桌面端（插件市场，不用命令行）</summary>

1. 打开 Codex 桌面端，进入 **插件** 页面。
2. 点右上角 **添加** → **添加插件市场**。
3. **来源** 填 `https://github.com/ahebbx/skills`，「Git 引用」和「稀疏路径」留空，点 **添加市场**。
4. 切到 **个人** 标签，会看到 **ahebbx-skills** 下的 4 个技能，点想要的技能右边的 **+** 安装。
5. 新开一个对话，直接问「今天吃什么」。

> ChatGPT 网页版没有插件市场，只能在 Skills 页面上传 [Releases](https://github.com/ahebbx/skills/releases/latest) 里的 `.skill` 安装包（Create → Upload from your computer），但网页版跑在云端，读写不到你电脑上的记录文件，「记得你吃过什么」只在当前对话里有效。

</details>

---

## 今天吃什么 (what-to-eat)

综合当天天气、你最近吃过什么、营养均衡和你的状态，直接告诉你这顿吃什么——1 个首选 + 2 个备选，每个都有贴合当天的理由，还会维护一份饮食日志，越用越懂你。

### 使用

安装后直接问：

- "今天中午吃什么？"
- "晚上吃啥，累了不想做饭"
- "早餐推荐一下，包子吃腻了"

第一次会问你城市和状态；之后它会查当天天气、避开你最近 3 天吃过的、照顾营养均衡。吃完说一声吃了什么，它会记进 `~/.what-to-eat/饮食记录.md`（不管在哪个 Agent、哪个项目里问都是同一份记录）——记录越多，推荐越准。告诉它忌口（"我不吃香菜"）会永久记住。

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

AI 会运行脚本找到最新的视频，在本地转写、抽帧，然后点评。也可以直接告诉它视频在哪：「点评一下 D:\录像\今天.mp4」。

**怎么录**

| 系统 | 推荐 | 说明 |
|------|------|------|
| macOS | QuickTime（文件 → 新建影片录制） | 录完忘了按 ⌘S 也没关系，脚本会从 QuickTime 未存储的录制里把视频抢救出来 |
| Windows | 系统自带「相机」应用 | 录好的视频默认在「图片\本机照片」，挪进 `视频\录视频练习`，或直接把路径告诉 AI |
| Linux | Cheese 或 OBS | 存到 `~/Videos/录视频练习`，或直接把路径告诉 AI |

**依赖**（只需装一次，缺什么脚本都会提示对应命令）：Python 3.8+、ffmpeg、whisper.cpp，外加一个 whisper 语音模型。

| 系统 | ffmpeg | whisper.cpp |
|------|--------|-------------|
| macOS | `brew install ffmpeg` | `brew install whisper-cpp` |
| Windows | `winget install Gyan.FFmpeg` | 到 [whisper.cpp Releases](https://github.com/ggml-org/whisper.cpp/releases) 下载 `whisper-bin-x64.zip`，解压后把文件夹加入 PATH |
| Linux | `sudo apt install ffmpeg`（或 dnf / pacman） | [从源码编译](https://github.com/ggml-org/whisper.cpp#quick-start)，把 `build/bin` 加入 PATH |

Windows 没有 Python 的话：`winget install Python.Python.3.12`。语音模型（约 1.6GB）让 AI 运行 `prepare.py --download-model` 自动下载，国内网络先设置环境变量 `HF_ENDPOINT=https://hf-mirror.com` 走镜像。

**配置**（可选环境变量）：`VIDEO_COACH_DIR` 视频目录、`VIDEO_COACH_MODEL` 模型路径、`VIDEO_COACH_WHISPER` whisper-cli 路径（不在 PATH 里时用）、`VIDEO_COACH_LANG` 转写语言（默认 zh）、`VIDEO_COACH_LOG` 练习日志路径。

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
ahebbx/skills
├── .claude-plugin/
│   └── marketplace.json              # Claude Code 插件市场清单（ahebbx-skills）
├── .github/workflows/
│   ├── test.yml                      # 每次推送在 macOS / Windows / Linux 上跑测试
│   └── release.yml                   # 推送 v* 标签时自动打包 .skill 并发布到 Releases
├── docs/superpowers/                 # 开发过程中的设计文档与实现计划
├── plugins/                          # 技能源码，一个技能一个目录
│   ├── what-to-eat/
│   │   ├── .claude-plugin/plugin.json    # 名称、简介、版本号
│   │   └── skills/what-to-eat/
│   │       ├── SKILL.md                  # 主流程
│   │       └── references/
│   │           ├── dishes.md             # 菜品库
│   │           └── seasonal.md           # 时令食材与天气对照
│   ├── video-coach/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/video-coach/
│   │       ├── SKILL.md                  # 双轨点评流程
│   │       └── scripts/
│   │           └── prepare.py            # 定位视频→抢救未存储→转写→抽帧（跨平台）
│   ├── daily-english-practice/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/daily-english-practice/
│   │       └── SKILL.md                  # 课程主流程
│   └── health-plan/
│       ├── .claude-plugin/plugin.json
│       └── skills/health-plan/
│           └── SKILL.md                  # 方案制定、打卡、复盘
├── scripts/
│   └── build-skills.sh               # 打包 dist/*.skill（Claude 桌面版 / 网页版安装包）
├── tests/
│   └── test_video_coach_prepare.py   # prepare.py 冒烟测试
├── .gitignore                        # 忽略 dist/、*.skill 等构建产物
└── README.md
```

## 发布

改完技能后打个版本标签推上去，GitHub Actions 会自动打包所有 `.skill` 并发布到 Releases：

```bash
git tag v1.2.0 && git push origin v1.2.0
```

本地预览打包结果：`./scripts/build-skills.sh`（输出到 `dist/`，已 gitignore）；本地跑测试：`python3 -m unittest discover tests`。

## License

MIT
