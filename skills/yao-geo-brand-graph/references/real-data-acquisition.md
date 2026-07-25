<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-brand-graph
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 真实数据获取与核验

本 skill 不把模型记忆当真实数据。正式报告必须先建立来源账本，再做 URL 连通核验和人工语义核对。

## 三层能力

| 层级 | 能力 | 产物 | 约束 |
| --- | --- | --- | --- |
| 来源登记 | 用户提供官网、产品页、投资者关系、监管文件、客户案例、媒体页或内部资料定位符。 | `evidence` 来源账本 | 没有来源的事实只能进入待确认项。 |
| 自动采样 | `scripts/collect_source_validation.py` 访问来源 URL，记录 HTTP 状态、页面标题、内容类型、核验时间。 | `source_validation` | 自动采样只能证明 URL 可达，不能证明事实主张语义完全正确。 |
| 语义核验 | 人工或 agent 对页面正文、日期、事实主张和图谱关系逐项比对。 | 实体、关系、三元组、JSON-LD | 页面不可见或无法授权的事实不能进入 JSON-LD 和正式图谱。 |

## 执行命令

```bash
python3 scripts/collect_source_validation.py \
  --input examples/hubspot-domestic-ai-test/report_input.json \
  --output examples/hubspot-domestic-ai-test/source-validation.generated.json \
  --update-input
```

## 判定规则

- `已连通`：URL 自动采样成功，可作为真实来源核验样本。
- `受限`：URL 返回 HTTP 错误或反爬限制，来源记录保留，但必须人工浏览或替换来源。
- `失败`：网络、超时或解析失败，不能作为自动核验证据。
- `跳过`：非 URL 定位符，需要内部系统、飞书知识库或人工文件核验。

## 报告规则

- 报告必须展示“真实数据来源核验”表。
- `source_validation` 数量应覆盖来源账本中的证据 ID。
- 自动连通数量越高，真实数据准备度越高；但任何核心事实仍必须用来源正文做语义核对。
- 国内 AI 平台采样结果不等同于事实来源，只能作为监测纠偏证据。
