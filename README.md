# 今天吃什么 (what-to-eat)

终结每天"吃什么"的纠结。一个 AI 技能（Agent Skill）：综合当天天气、你最近吃过什么、营养均衡和你的状态，直接告诉你这顿吃什么——1 个首选 + 2 个备选，每个都有贴合当天的理由，还会维护一份饮食日志，越用越懂你。

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
```

### Claude 桌面版 / claude.ai

下载本仓库里的 [what-to-eat.skill](./what-to-eat.skill)，发到 Claude 对话里，点卡片上的 **Save skill** 即可。

## 使用

安装后直接问：

- "今天中午吃什么？"
- "晚上吃啥，累了不想做饭"
- "早餐推荐一下，包子吃腻了"

第一次会问你城市和状态；之后它会查当天天气、避开你最近 3 天吃过的、照顾营养均衡。吃完说一声吃了什么，它会记进 `~/.what-to-eat/饮食记录.md`（家目录统一路径，Claude Code / Codex 等工具、任何项目里问都是同一份记录）——记录越多，推荐越准。告诉它忌口（"我不吃香菜"）会永久记住。

## 结构

```
├── .claude-plugin/
│   └── marketplace.json          # 插件市场清单（ahebbx-skills）
├── plugins/what-to-eat/
│   ├── .claude-plugin/
│   │   └── plugin.json           # 插件元信息
│   └── skills/what-to-eat/
│       ├── SKILL.md              # 主流程
│       └── references/
│           ├── seasonal.md       # 时令食材、天气→饮食映射
│           └── dishes.md         # 菜品库（快手菜/硬菜/外卖/早餐）
└── what-to-eat.skill             # Claude 桌面版一键安装包
```

## License

MIT
