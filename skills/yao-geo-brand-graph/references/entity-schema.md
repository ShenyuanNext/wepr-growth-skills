<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-brand-graph
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 实体与关系 Schema

## 实体字段

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `id` | 是 | 稳定 ID，建议使用 `type:slug`。 |
| `type` | 是 | 品牌、产品、服务、功能、技术、行业、用户、场景、客户、案例、证据、地点、时间、人物、团队、证书、合作伙伴。 |
| `name` | 是 | 规范名称。 |
| `aliases` | 否 | 简称、英文名、旧名、产品线名称和常见误写。 |
| `description` | 是 | 可验证事实描述，不写空泛口号。 |
| `source_ids` | 是 | 来源账本中的证据 ID。 |
| `confidence` | 是 | 官方事实、第三方证据、媒体描述、用户反馈、推断、待确认。 |
| `privacy_review` | 是 | 公开、已授权、匿名化、待确认、不可公开。 |

## 关系字段

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `subject` | 是 | 主体实体 ID。 |
| `predicate` | 是 | 拥有、提供、适用、合作、获得、引用、服务、对比、替代、来源、时间。 |
| `object` | 是 | 客体实体 ID。 |
| `direction` | 是 | 明确方向，如 `brand:a -> product:b`。 |
| `evidence_ids` | 是 | 至少一个证据 ID。 |
| `confidence` | 是 | 可信等级。 |
| `notes` | 否 | 边界条件、授权条件或页面补强说明。 |
