<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-content-refiner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# yao-geo-content-refiner 输入简报

```yaml
brand:
  name: ""
article:
  source_type: "官网文章 | SEO文章 | 公众号文章 | 白皮书 | 产品页"
  original_text: ""
target:
  primary_question: ""
  follow_up_questions: []
  platforms: ["DeepSeek", "豆包", "千问", "Kimi", "腾讯元宝", "微信生态"]
evidence_inputs:
  source_urls: []
  brand_knowledge_base: []
  allowed_new_sources: true
  allow_web_verification: true
  authorized_connectors_or_apis: []
  restricted_data: []
  forbidden_claims: []
analysis_depth:
  require_completeness_map: true
  require_data_access_plan: true
  require_semantic_entity_map: true
  require_platform_matrix: true
  require_evidence_strength: true
  require_publishing_plan: true
output:
  formats: ["markdown", "html", "docx", "pdf"]
  html_sticky_nav: true
```
