# ALL KONJAC 三语统一发布记录

## 发布范围

已合并 2026-10-16 图片/质量参考版本、三语 SEO/GEO 版本，以及「深度学习并撰写GEO博客」对话认可的精粉与胶对比文章。统一源：本仓库 origin/main；实施工作树为 work/allkonjac-kgm-release-2026-10-19。后续编辑先从最新 main 合并，不以旧工作树直接覆盖生产站。

39 个 canonical URL：15 业务页、18 篇文章、3 Blog 栏目、3 COA 参考页。英/泰/印尼语各 13 页。原始图片不重新编辑，恢复此前批准的现成文件；3D 保留在烘干线页面。

## 内容边界与翻译

COA 保留 17 条历史报告项目、1 条单独标注的供应商更新。93% 未包装成修订实验室报告；0.04 mg/kg 是定量限，不是实测浓度。文件不构成制造商正式批次 COA。三语数据使用同一数据源。

Google 原始译文、术语校准覆盖和最终译文分别保存在 source/data/quality-google-raw.json、quality-editorial-overrides.json、quality-translations.json。校准品牌名、年份、批次/导航/干片术语和供应商更新说明。数字与品牌不允许翻译漂移。泰语和印尼语尚未经母语行业专家审校，此项不冒充已完成。

## 验收

- 生成器 self-test、check 与输出构建通过。
- 39 页静态链接、canonical、三语关联、JSON-LD、站点地图、事实索引校验通过。
- 公开文本无中文检查通过；32 张业务图片和 10 张豁免图片哈希检查通过。
- 39 页 390/1440px、禁用 JavaScript 的可读性与无横向溢出检查通过。
- 三语 360/390/768/1440px 的质量卡片、COA 17+1 数据行、数字、同页语言切换、干片图片及放大交互通过。
- 三语对比文章 12 个视口/路由场景通过；引用和表格检查通过。
- 烘干线 3D 28 项检查通过，包含旋转、键鼠触控、缩放、九视角、减少动态效果和 WebGL 不支持时回退。
- Wrangler dry-run 通过；内部 source/content/scripts/audits 目录排除部署。

对应 JSON：unified-static-2026-10-21.json、release-browser-2026-10-21/report.json、unified-browser-2026-10-21/report.json、unified-3d-2026-10-21/browser-verification.json、comparison-2026-10-20/browser.json。

## 回退与线上确认

发布前线上 Worker：20c60899-51ce-4ef3-a005-8cce1e631dbe，远端源码 1b0895948c5232301b5cf904df90c5d43e59f521。若生产访问出现严重故障可使用 Wrangler rollback 指定该版本；该旧版本缺少本轮新增内容，只用于紧急恢复。

当前阶段：本地验收完成，线上发布及全量复核结果在完成后追加。

## 效果观察

沿用 audits/seo-geo-release-2026-10-20.md 的已记录搜索基线与 24 题 AI 观察集，不把历史记录称为实时指标。以实际统一上线日期为第 0 天，在第 2/6/12 周复核；不自动新增定时任务。有效询盘需业务类别、具体需求、目标市场和可回复联系方式。没有采集的数据标为缺失。

hbhpmy 不在此次发布范围。
