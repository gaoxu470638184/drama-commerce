# drama-commerce · 短剧带货

> 把「商品」装进「剧情」里的 Agent Skill。从一句商品描述，跑到可投放的竖屏成片。

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-4B32C3)

![Version](https://img.shields.io/badge/version-1.0.0-blue)

![Language](https://img.shields.io/badge/lang-zh--CN-red)

适用于 **Claude Code / WorkBuddy / Cursor / 任何支持 Agent Skills 规范的工具**。

---

## 这是什么

短视频带货最大的坑不是「不会拍」，而是**拍到第 5 条才发现钩子不成立**。这个 Skill 把短剧带货拆成七个可交付、可验收的步骤，每一步产出落盘文件，任何一步不通过就不进入下一步——把「凭感觉拍」变成「按流程测」。

它不生成视频，它生成**能直接喂给视频模型和剪辑工具的全部上游物料**：卖点、钩子、剧本、分镜表、逐镜头提示词、配音脚本、自检报告。

```
输入商品 → 卖点提炼 → 钩子设计 → 剧本 → 分镜表 → 制作方案 → 自检交付
```

## 核心设计原则

| 原则            | 含义                                      |
| ------------- | --------------------------------------- |
| **剧情是壳，卖点是核** | 前 3 秒只留人、不提商品；商品只在情绪最高点或「解药」位置植入        |
| **反精致**       | 带货视频要像「有人随手拍」，不要像广告。首帧质感、手持感、原生字幕 > 电影感 |
| **一条钩子一条命**   | 每条片只验证一个钩子假设，批量做变体，而不是一条片塞满卖点           |
| **成本分级**      | 能用代码/素材合成的，绝不用视频模型烧钱；模型只生成「必须动起来」的碎片    |

## 七步流程

| 步骤     | 动作                                    | 产出                       |
| ------ | ------------------------------------- | ------------------------ |
| 1 输入收集 | 商品 / 人群 / 平台 / 形态 / 数量                | `00-brief.md`            |
| 2 卖点提炼 | 1 主卖点 + 2-3 辅助卖点，全改写成「人话场景」+ 痛点-解药映射表 | `01-selling-points.md`   |
| 3 钩子设计 | 从 8 个钩子公式选 3-5 个，每个写前 3 秒，过自检才留       | `02-hooks.md`            |
| 4 剧本   | 固定五拍：钩子 → 共鸣 → **反转植入** → 见证 → 转化     | `03-script-epNN.md`      |
| 5 分镜表  | 逐镜头标注景别/运镜/素材来源/商品出现方式                | `04-shotlist-epNN.md`    |
| 6 制作   | 按镜头分流：AI 生成 / 真图推镜 / TTS / 剪映或 ffmpeg | `05-production-notes.md` |
| 7 自检   | 违禁词红线 + 病毒度评分（≥7/10 才交付）+ A/B 变体      | `06-review.md`           |

## 安装

### 方式一：一行命令（自动探测目录）

```bash
git clone https://github.com/gaoxu470638184/drama-commerce.git /tmp/drama-commerce
cd /tmp/drama-commerce && ./install.sh
```

Windows PowerShell：

```powershell
git clone https://github.com/gaoxu470638184/drama-commerce.git $env:TEMP\drama-commerce
cd $env:TEMP\drama-commerce
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

安装脚本会自动探测 `.workbuddy/skills` 或 `.claude/skills`，同名旧版本自动备份为 `.bak.<时间戳>`，不会丢东西。

### 方式二：手动放置

```bash
git clone https://github.com/gaoxu470638184/drama-commerce.git

# WorkBuddy
cp -r drama-commerce ~/.workbuddy/skills/

# Claude Code
cp -r drama-commerce ~/.claude/skills/

# Cursor / 其他：放进该工具的 skills 目录即可
```

### 方式三：项目级（只对单个项目生效）

```bash
cp -r drama-commerce <你的项目>/.workbuddy/skills/
```

安装后**重启会话**，Skill 即生效。

## 使用

直接在对话里说：

```
帮我做一条短剧带货视频
商品：便携榨汁杯、89 元、核心卖点 30 秒出汁、刀头不用拆洗
人群：25-35 岁上班族女性、办公室下午茶
平台：抖音
形态：实拍混剪 + 口播
数量：3 条（3 个钩子变体）
```

Skill 会自动按七步推进，并在每一步停下来等你确认。

也可以只调用其中一环，例如：

- 「用这个商品写 5 个前 3 秒的钩子变体」
- 「把这个剧本拆成分镜表，标出哪些镜头可以图生视频」
- 「按这套分镜写即梦 Seedance 的逐镜头提示词」
- 「按自检清单给这条片打分，指出最该改的地方」

## 仓库结构

```
drama-commerce/
├── SKILL.md                         主流程定义（Agent 读这个）
├── references/
│   ├── hook-formulas.md             8 个钩子公式 + 卖点提炼法
│   ├── shot-list-guide.md           分镜规范 + 商品植入规则
│   ├── video-prompt-dialects.md     即梦 Seedance / 可灵 / Veo 提示词方言
│   └── delivery-checklist.md        违禁词红线 + 病毒度评分表
├── examples/nut-gift-box/           完整实战案例：坚果礼盒 3 条片全流程产出
├── scripts/validate.py              仓库自检（frontmatter / 死链）
└── install.sh / install.ps1         跨平台安装脚本
```

## 实战案例

[`examples/nut-gift-box/`](examples/nut-gift-box/) 是一份**未经修饰的真实产出**：59.9 元坚果礼盒、视频号、AI 生成剧情、3 条片。包含 brief、卖点表、8 个钩子、3 份完整剧本、3 份分镜表、制作方案、自检报告，以及一份剪辑踩坑记录（含 ffmpeg 实战参数）。

看它比看文档快——尤其 `08-cut-notes.md` 记了 4 个真实踩坑（SAR 像素比导致 concat 失败、中文字幕超边界、AI 水印去除等）。

## 已知限制（诚实版）

1. **AI 一定画不对包装文字**。任何把商品交给视频模型的镜头，包装上的文字都会变成乱码。正确做法是：商品特写用**真图定格 + ffmpeg 缓慢推镜**，零失真零成本；模型只负责人物和氛围。
2. **视频模型按条计费**。Skill 会在执行前列出预计条数和费用并等你确认，但费用本身由你自己的账号承担。
3. **违禁词只能查通用红线**。医疗、保健、金融类商品的平台白名单更新频繁，最终需人工按平台规则复核。
4. **不替你做投放决策**。它给钩子假设和 A/B 变体，但哪个跑得动，得看你的实际投放数据。

## Roadmap

- [ ] 补充小红书、TikTok 的平台差异配置
- [ ] 增加数字人口播（A-roll）分支流程
- [ ] 提供剪映草稿（draft）生成脚本
- [ ] 增加转化数据回填 → 钩子效果归因模板
- [ ] English version

## 贡献

欢迎 PR 和 Issue。最需要的贡献是：**真实投放数据验证过的钩子公式**和**各平台规则更新**。提交前请跑一遍 `python scripts/validate.py`。

详细约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 合规与免责

- 本仓库只提供方法论与提示词模板，不含任何商品素材、视频文件或第三方商标内容。
- 案例中的价格、规格仅为示例，实际投放内容须与商品真实信息一致。
- 使用者需自行确保：所用 IP 已获授权、素材为自有或已授权、内容符合目标平台规则与当地广告法。
- 作者不对使用本 Skill 产生的投放结果、平台处罚或法律纠纷承担责任。

## 致谢

设计思路参考了 Agent Skills 生态中的若干公开实践（剧情管线、UGC 反精致广告、剪映自动化），并经实际项目打磨后重新组织成七步流程。

## License

[MIT](LICENSE) · 可商用、可修改、可分发，保留版权声明即可。
