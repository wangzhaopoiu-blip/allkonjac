

## 2026-10-20 三语正式发布与语言清理（最新状态，以本节为准）

用户已表示英文预览“效果可以”，并要求所有语言网页正文、菜单、引用、元数据和字体设置不出现中文；明确保留原图片。本轮已完成谷歌翻译、专业术语校对与正式发布，先前“新文章未发布／等待审阅”的记录仅为历史状态。

### 已上线 URL

- https://allkonjac.com/blog/konjac-refined-powder-vs-konjac-gum/
- https://allkonjac.com/th/blog/konjac-refined-powder-vs-konjac-gum/
- https://allkonjac.com/id/blog/konjac-refined-powder-vs-konjac-gum/
- 对应博客列表：https://allkonjac.com/blog/ 、https://allkonjac.com/th/blog/ 、https://allkonjac.com/id/blog/

### 发布与验收证据

- Git 正式内容提交 `7af7680` 已推送 origin/main；以已有 main `7dc7598` 为基础，保留同期烘干线 3D 查看器更新。
- Cloudflare Worker `allkonjac` 版本 `b38856f6-c8d9-4873-8e14-dfe502c284e0`，发布成功，日期为真实发布日 2026-10-20。
- 三语文章与列表在 390/1440 宽度共 12 项线上页面检查通过，均 HTTP 200；目录、引用锚点、手机菜单、表格、canonical 与四个真实语言替代链接通过。
- 全站 49 个公共文本资源线上检查通过：无中文文字／中文字体声明，排除 Cloudflare 原有统计脚本后与本机内容一致。全站 28 个 HTML 的本机链接及锚点无缺失。
- 各语言已接入博客列表、语言切换、站点地图（26 个 canonical URL）及 llms；原采购指南保留并互链。
- 原图、水印、二维码说明未修改；中文内部稿未部署。
- 谷歌翻译实际输出与校对记录保存在源码 `source/comparison/`，该目录被静态发布排除。

### 交付与下一步

- 本机三语预览及 ZIP：`C:/Users/wangzhao/Documents/ChatGPT/零星琐碎/ALLKONJAC三语博客发布包_2026-10-20`，入口为 `打开预览.html`。web 全部 noindex；直接离线打开三语页面、字体与菜单测试通过。
- 发布源码：`D:/Codex/Projects/ChatGPT/外贸网站/work/allkonjac-language-policy-2026-10-20`，与旧工作树的未提交本地化草稿隔离。
- 验证详情：源码 `audits/comparison-2026-10-20/` 及交付包 `qa/`。
- hbhpmy.com 仍等待域名控制权与发布入口；中文核验稿保存在交付包 `internal/article.zh.md`，不重复催要，本周之后仍无入口时按约定于 2026-10-26 询问一次。
- 每日跟进继续，仅在实际进展、异常、失败或需要用户行动时通知；提示词已更新到本次正式发布状态。
