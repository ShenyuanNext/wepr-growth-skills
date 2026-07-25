<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-brand-graph
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 研究支撑框架

本 skill 采用“知识图谱 + 实体链接 + 证据治理 + 结构化数据一致性”的组合框架。

- Hogan, A. et al. “Knowledge Graphs.” https://arxiv.org/abs/2003.02320
- W3C. “RDF 1.1 Concepts and Abstract Syntax.” https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/
- W3C. “JSON-LD 1.1.” https://www.w3.org/TR/json-ld11/
- W3C. “PROV-O: The PROV Ontology.” https://www.w3.org/TR/prov-o/
- W3C. “Shapes Constraint Language (SHACL).” https://www.w3.org/TR/shacl/
- W3C. “SKOS Simple Knowledge Organization System.” https://www.w3.org/2004/02/skos/specs
- Schema.org. “Organization.” https://schema.org/Organization
- Schema.org. “SoftwareApplication.” https://schema.org/SoftwareApplication
- Google Search Central. “Intro to how structured data markup works.” https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- Shen, W., Wang, J., Han, J. “Entity Linking with a Knowledge Base: Issues, Techniques, and Solutions.” https://doi.org/10.1109/TKDE.2014.2327028

落地规则：

- RDF 约束三元组和方向：关系必须能写成 subject-predicate-object，方向不可省略。
- JSON-LD 约束结构化输出：JSON-LD 是 Linked Data 的 JSON 序列化，只承载页面正文已写明且可验证的事实。
- PROV-O 约束证据治理：每条核心关系都要能追溯来源、日期、核验状态和使用方式。
- SHACL 思路约束质量门：把必要字段、实体类型、证据 ID、表格排版和输出文件存在性做成可检查规则。
- SKOS 约束别名和旧名：把简称、英文名、旧名、行业词和易混词视为受控词表，而不是自由文本。
- Schema.org 与 Google 结构化数据约束页面一致性：结构化数据不得描述页面不可见或未支撑的事实。
- 实体链接研究约束消歧流程：按 mention -> candidate -> canonical entity 处理品牌名、产品名、人名、地点和客户案例。
