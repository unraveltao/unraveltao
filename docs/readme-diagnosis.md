# 现状诊断 — unraveltao/unraveltao

采集时间：2026-10-26。原始文件见 `README.baseline.md`（与线上 main 分支一致）。

## 一、事实基线

| 项 | 值 |
|---|---|
| 仓库 | `unraveltao/unraveltao`（profile 仓库，公开） |
| README 大小 | 7.2 KB，单文件，无本地图片（除 `assets/bar_graph.png`） |
| 文件结构 | `README.md`、`assets/bar_graph.png`、`.github/workflows/waka_readme_status.yml` |
| README 最后更新 | 2024-08-25（waka 段自报 `25/08/2024 01:13:04 UTC`） |
| 公开仓库数 | 15，全部 0 star；仅 `lattice` 有 1 fork |
| 最近推送 | `lattice` 2026-10-25、`lattice-registry` 2026-10-25、`Notes` 2026-10-20，其余多在 2024 年 |
| 个人资料 | name: Iron Tom；location: China；twitter: iron_tom233；bio 写到 "creating " 处截断 |

## 二、硬故障（读者会直接看到破图）

| 问题 | 位置 | 后果 |
|---|---|---|
| `github-readme-streak-stats.herokuapp.com` | stats 行第二张卡 | Heroku 免费 dyno 已于 2022 年停止，该域名基本返回错误 → 硬降级 |
| `github-readme-stats.vercel.app` 公共实例 | 统计卡、语言卡 | 长期限流，间歇性 `Something went wrong` → 硬降级 |
| `assets/bar_graph.png` 依赖 waka workflow 每周覆写 | Waka 段 | workflow 已 14 个月未产出，图与文字停在 2024-08 |
| Waka 段时区 `America/Los_Angeles` | Waka 段 | 与"China"身份矛盾，数据解释错误 |

## 三、内容失真（比破图更伤）

1. **旗舰项目缺席。** `lattice`（棂，Tauri 2 + React 19，约 22K 行 TS + 23K 行 Rust，17 个官方 widget，MIT）是唯一有实质工程量、有 fork、昨天还在提交的项目，README 里一个字都没有。访客看完只会记得"一个用 Go/React/Docker 的人"。
2. **About Me 停留在 2024。** 写着 "currently working on building a personal blog using Next.js"、"learning Advanced React hooks" —— 与当下的 lattice（Rust/Tauri/沙箱权限模型/本地 AI）完全错位。
3. **技术栈图标与真实工作不符。** 15 个图标里 MUI、Ant Design、Figma、Vite、HTML5、CSS3 属于"用过"，而 Tauri、Rust、WebView2 这些真正在写的没有。
4. **统计口径自相矛盾。** "179 Contributions in the Year 2024" 与 2026 年仍在活跃的事实冲突；`📦 ? Used in GitHub's Storage` 是占位符残留。

## 四、结构问题

- **信息层级倒置。** 首屏是打字机动画 + 访问计数 + 奖杯墙 + 两张统计卡，四层组件之后才出现"你是谁"。3 秒扫描的访客拿不到任何有效信息。
- **组件过载。** trophy（7 列）+ stats + streak + top-langs + roadmap.sh 卡片 + 15 个图标 + Waka 四张 ASCII 表，同屏竞争注意力，没有一个胜出。
- **零 star 却挂奖杯墙。** 奖杯按 star/commit/PR/issue/关注者分级，0 star、1 follower 时渲染出来是空奖杯或铜牌，属于自曝其短。
- **无行动入口。** 没有"看我的项目""读我的笔记""联系我"的明确路径，邮箱埋在 About Me 第五条。

## 五、结论

这份 README 是 2024 年的"组件收集型"主页：装饰齐全、内容为空。改造方向不是换更多组件，而是**先立内容骨架（旗舰项目 + 一句话定位 + 行动入口），再让组件去佐证**。
