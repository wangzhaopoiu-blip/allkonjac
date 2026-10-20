# ALL KONJAC SEO/GEO 发布与复测记录

记录日：2026-10-20。范围：英文、泰文、印尼文各 5 个业务页和 6 个 Blog 页，共 33 个规范 URL。最终目标是来自目标市场的有效询盘，须同时包含业务类别、产品或项目需求、目标市场和可回复的联系方式。按钮点击只能算意向动作。

## 发布前基线

| 指标 | 状态 | 后续数据源 |
| --- | --- | --- |
| Search Console 28 天按国家、查询和页面的展现与点击 | 2026-10-20 界面显示全站 2 次点击、12 次展现；中国 2/2、印尼 0/4、泰国未出现，其他国家各 0–2 次展现。页面维度及英文目标查询分组待记录；图表实际有数据的日期为 10 月 5–17 日 | Search Console 效果报告，继续核对页面与目标查询 |
| Search Console 收录 | 2026-10-20 概览显示 15 页已收录、5 页未收录；报告口径及具体 URL 待核 | Search Console 网页索引报告 |
| 业务页访问与联系点击 | 基线缺失；未取得分析数据 | 经同意配置的站点分析或服务器日志 |
| 实际有效询盘 | 基线缺失；不得以点击推算 | 人工询盘登记与后续资格审核 |
| 固定问题集中的 AI 提及与引用 | 基线缺失；尚未实测 | 按下列 24 题在固定模型与日期记录 |

询盘登记字段：日期、国家、语言、来源 URL、业务线、需求摘要、联系方式是否可回复、首次响应时间、是否有效、无效原因、商机阶段。联系方式只放在有权限的业务系统，公开审计文件不记载私人联系方式。

## 固定 AI 买家问题集

每次在同一模型、地区设置与无历史会话下提问，保存日期、原文回答、品牌提及、事实是否准确、引用 URL 和错误类别。以下每行两题，合计 4 条业务线 × 3 种语言 × 2 题。

| 业务 | 语言 | 问题 1 | 问题 2 |
| --- | --- | --- | --- |
| 原料 | en | How should I choose konjac powder, refined konjac powder or konjac gum for a food product? | What information should I send a konjac ingredient supplier before requesting a grade and sample? |
| 原料 | th | ควรเลือกแป้งบุก ผงบุกบริสุทธิ์ หรือกัมบุกสำหรับผลิตภัณฑ์อาหารอย่างไร? | ควรส่งข้อมูลอะไรให้ผู้ขายวัตถุดิบบุกก่อนขอเกรดและตัวอย่าง? |
| 原料 | id | Bagaimana memilih bubuk konjak, bubuk konjak rafinasi, atau gum konjak untuk produk pangan? | Informasi apa yang perlu saya kirim kepada pemasok bahan konjak sebelum meminta grade dan sampel? |
| 食品设备 | en | What should a konjac food equipment project brief include? | How can I compare a reference equipment configuration with my factory requirements? |
| 食品设备 | th | เอกสารข้อมูลโครงการเครื่องจักรอาหารบุกควรมีอะไรบ้าง? | จะเปรียบเทียบรูปแบบเครื่องจักรอ้างอิงกับความต้องการของโรงงานอย่างไร? |
| 食品设备 | id | Apa saja yang perlu ada dalam ringkasan proyek peralatan pangan konjak? | Bagaimana membandingkan konfigurasi peralatan referensi dengan kebutuhan pabrik saya? |
| 干片烘干线 | en | What conditions matter when planning a konjac dried-chip drying line? | What material, output and utility data should I provide for a drying-line quotation? |
| 干片烘干线 | th | ต้องพิจารณาเงื่อนไขใดเมื่อวางแผนสายการอบชิ้นบุกแห้ง? | ต้องให้ข้อมูลวัตถุดิบ ผลผลิต และสาธารณูปโภคใดเพื่อขอใบเสนอราคา? |
| 干片烘干线 | id | Kondisi apa yang perlu dipertimbangkan saat merencanakan lini pengeringan irisan konjak? | Data bahan, hasil, dan utilitas apa yang diperlukan untuk meminta penawaran lini pengeringan? |
| 应用技术 | en | How should I test konjac glucomannan for texture and stability in my food formulation? | Which trial details are needed before discussing konjac application development? |
| 应用技术 | th | ควรทดสอบ KGM ด้านเนื้อสัมผัสและความคงตัวในสูตรอาหารอย่างไร? | ต้องเตรียมข้อมูลการทดลองใดก่อนหารือการพัฒนาการใช้บุก? |
| 应用技术 | id | Bagaimana menguji KGM untuk tekstur dan stabilitas dalam formulasi pangan saya? | Rincian uji apa yang diperlukan sebelum membahas pengembangan aplikasi konjak? |

## 上线后诊断

2026-10-20 已部署 Cloudflare Worker 版本 `1f88a4ef-0b3d-4060-86b5-1f56e30e875a`。线上 33 个规范 URL 均返回 200，正文与本地生成文件逐字节一致；两条含查询参数的 HTTP 示例均 301 至相同路径和参数的 HTTPS；未知路径返回真实 404。未向搜索引擎手动提交收录请求。

- 第 2 周：逐页核查抓取响应、HTTP→HTTPS 301（含路径与查询参数）、真实 404、canonical、站点地图抓取、联系入口记录。若未发现页面，检查内部链接和服务器响应，再复查。
- 第 6 周：按国家和语言对照收录、实际查询与内容匹配。已收录却无目标查询时，按真实用词补应用条件和选型依据；有展现但点击弱时，核对标题和摘要与正文承诺。
- 第 12 周：同口径比较搜索、固定 AI 问题集和有效询盘。若访问有了但无有效询盘，核查移动联系路径、可提供文件、回复速度和询盘质量。样本小时只记录趋势。
- AI 答案误述品牌或业务时，先核对站内主体信息与可抓取事实，再争取真实编辑引用。`llms.txt`、外链数量或锚文本比例均不保证推荐。
- 页面慢时，先记录同设备和网络条件下的核心网页指标、图片传输量及 3D 加载，再改动瓶颈并复测。本轮静态资源盘点发现原有部分 JPG 为 500–865 KB、设备 3D 脚本约 546 KB；尚无现场性能指标，不据此宣称用户流失原因。

## 资料与内容待核

- 泰文、印尼文新增业务清单和 Blog 已通过生成器与文本检查，仍需母语行业审校术语及文风。上线后的修订应记录日期，实质文章更新时再修改 `dateModified`。
- 本轮没有新增照片；既有 `drying-line-wide.jpg`、`drying-line-wide-2.jpg`、`drying-drive.jpg`、`food-equipment.jpg` 的精确来源哈希与公开授权记录未在共享素材目录中找到。现有水印与此前上线审批不等于来源权属已核实。公开文案已改为工业参考图表述，后续应补原件、权属及使用范围记录。
- 所有认证、法律主体关系、产能、客户成果和产品性能仍以可核实原始资料为准，不从研究论文或示意图外推。
