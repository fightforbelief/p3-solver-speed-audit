# P3 首投决定与上传清单

**首选 Operations Research Letters（ORL），按理论方法短文准备。** 投稿版以一个可独立表述的组合优化问题为中心。读者只要知道各项成本、正标签总数和查询预算，就能使用定理选出最优查询，并给出精度保证。该刊明确接受有方法基础的应用与纯方法研究，篇幅上限为八个期刊页。本稿用 Elsevier 的双栏类编译为三页。该刊 2026 年发表的付费查询决策树短文，也有面向该问题的读者。[期刊范围](https://shop.elsevier.com/journals/operations-research-letters/0167-6377) · [同刊实例](https://doi.org/10.1016/j.orl.2025.107370)

## 创新性判断

- **值得送审的贡献**是固定基数的二元标记如何改变最优查询。排序后的连续保留块给出精确解。多数应答的对手构造同时给出顺序查询和跨组自适应分配的下界。稿件还给出了相邻窗口的差分公式，以及分组边际贪心可任意偏离最优的四项加两项反例。
- **已有基础**包括固定边际下的重排极值、用背包处理带成本的总和查询、按组预算做动态规划。稿件引用了 Olston 和 Widom 的早期工作，将异价困难性限定在已知总数甚至恰有一半正标记的情形。Chen 等研究查询后如何选择下游解，Zhuo 和 Nagarajan 研究按查询成本识别假设。本文的损失是可行总和的最坏区间宽度。此次定向文献核对支持这样的区别，但不能排除其他领域已有等价结果。[总和查询先例](https://www.sigmod.org/publications/dblp/db/conf/vldb/OlstonW00.html) · [稳健选择](https://doi.org/10.1016/j.dam.2025.12.012)
- **实验证据足以支持应用示例。** 六个场景、3,968 个共同求解成功实例、三个时间片，另有 4,695 个完整测试实例的超时计费敏感性。六个主场景在 10% 核查预算下都与“只查最慢”打平。合并 394 次核查时，精确解对按实例数分配改善 43.8%，对按基准耗时分配改善 2.0%，逐次贪心在三个时间片均达到同一精确解。原始主表经独立代码重算；两条新增分配基线是同一批数据上的事后敏感性比较。
- **主要审稿风险**是固定总数、可恢复真值、加性冷启动三个条件限制适用范围，且现实日志丢失配对的频率未知。模拟屏蔽能检验识别区间，不能证明部署加速，也不能证明新算法在真实场景中普遍胜过贪心。相比同样有信息获取研究的 *Discrete Applied Mathematics*，本稿以一个短定理和可复现实例组成，ORL 的短篇方法定位更合适。我的判断是可以首投，是否送外审仍取决于编辑对问题普适性的评价。[相关期刊实例](https://doi.org/10.1016/j.dam.2025.12.012)

## 投稿文件

| 用途 | 文件 |
| --- | --- |
| 稿件与可编辑源码 | [编译 PDF](manuscript.pdf) 和[单文件 LaTeX 源码](manuscript.tex)，使用 elsarticle，无外部图表或文献库依赖 |
| 给编辑的投稿信 | [cover-letter.docx](cover-letter.docx) |
| 四条研究亮点 | [highlights.docx](highlights.docx) |
| 利益声明文本 | [declaration-of-interests.docx](declaration-of-interests.docx) |
| 可随稿上传的补充材料 | [replication.zip](replication.zip)，含脚本、原始结果表、哈希和复现说明，可独立于项目仓库使用 |

标题、作者、通讯邮箱、单段英文摘要和关键词均在主稿首页。期刊八页上限和出版社亮点、AI 披露政策已核对。期刊专属在线 Guide 在本次访问返回 HTTP 403，系统里的文件类别、声明工具与个别必填字段请以登录时显示为准。若要求工具生成的利益声明，由通讯作者通过官方工具签发。随稿主文已说明 Codex 参与选题与证明、代码、撰写和投稿材料。两位作者在正式递交前需核定论文、披露与作者贡献，确认同意投稿和同期投稿状态。此目录是备投稿件。[期刊作者指南](https://www.sciencedirect.com/journal/operations-research-letters/publish/guide-for-authors) · [亮点规范](https://www.elsevier.com/en-au/researcher/author/tools-and-resources/highlights) · [AI 政策](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals) · [利益声明工具](https://declarations.elsevier.com/)
