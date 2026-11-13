# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-11-13

首个公开版本。

### 新增

- `SKILL.md`：短剧带货七步流程（输入收集 → 卖点提炼 → 钩子设计 → 剧本 → 分镜表 → 制作 → 自检交付）
- `references/hook-formulas.md`：8 个钩子公式 + 卖点提炼与场景化改写方法
- `references/shot-list-guide.md`：分镜表规范、商品植入规则、废镜头判定
- `references/video-prompt-dialects.md`：即梦 Seedance / 可灵 / Veo / Sora 提示词方言与约束尾写法
- `references/delivery-checklist.md`：违禁词红线、病毒度 10 分制评分表
- `examples/nut-gift-box/`：坚果礼盒 3 条片完整实战案例（含 ffmpeg 剪辑踩坑记录）
- `install.sh` / `install.ps1`：跨平台安装脚本，自动备份旧版本
- `scripts/validate.py` + GitHub Actions：frontmatter、死链、孤儿文件、编码自检

### 已知问题

- AI 视频模型无法正确绘制商品包装文字，商品特写需走「真图定格 + 推镜」方案
