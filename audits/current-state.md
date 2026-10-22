# ALL KONJAC 当前短交接

更新：2026-10-22（北京时间）。后续从最新 origin/main 开始；不要把旧预览工作树整站覆盖上线。

- 当前发布源码工作目录：`D:/Codex/Projects/ChatGPT/外贸网站/work/allkonjac-buyer-quotation-2026-10-21`。公开站点源码提交 `8972eb8`；后续记录提交只更新验收资料。
- 生产 Worker：`018a5b4c-ca02-435a-a597-5b9d4b493df2`。已完成五项采购/询盘优化及英、泰、印尼语匿名报价示范。39 个 canonical 页面保留；3 个 PDF 为附加下载资源，使用 noindex 响应头。
- 发布包 106 文件；线上 105 个非404文件与本地一致，真实404另行验证。三语询盘复制/预填/下载15组检查、线上3D28项检查均通过。未发送询盘测试。
- 记录：`audits/buyer-quotation-release-2026-10-22.md`；来源与翻译限制：`audits/buyer-quotation-provenance.md`；人工询盘台账：`audits/enquiry-ledger.md`。
- 构建后必须运行 `python scripts/package_public.py`；Wrangler 现在只部署 `.wrangler/public`，不能直接部署整个源码根目录。对待发布源码运行生成器、静态检查及对应浏览器验收；先核对远端和差异。
- 回退版本：`1507c738-e7c4-406d-8bec-a5161cff2ae0`，即此次发布前实测版本；旧交接中的 `a158088d...` 并非最近回退点。发布前102个文件与基准 `64270f7` 一致。
- 旧目录 `work/allkonjac-kgm-release-2026-10-19` 的零食参考预览及未提交修改保留，未纳入本轮。不要从旧预览目录直接发布；其中未跟踪的旧交接文件应先保留，再考虑合并主分支。
- 泰语和印尼语母语行业审校尚未完成。未取得的现行等级/批次/交付证明、法律审查、搜索/AI/真实询盘数据不能声称已验证。保留原2026-10-21基线及11月4日、12月2日、2027年1月13日观察节点，另记本次10月22日内容发布。
- hbhpmy 不在本轮范围。没有新增自动化、外联、付费链接或搜索提交。

三语报价入口：`/ingredients/#quotation-example`、`/th/ingredients/#quotation-example`、`/id/ingredients/#quotation-example`。公开PDF原件仅匿名示例；用户的来源报价原件仍在Downloads并已登记共享索引，未上传。
