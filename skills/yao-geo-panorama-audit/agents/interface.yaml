# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-panorama-audit
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

interface:
  display_name: "Yao GEO 全景诊断"
  short_description: "基于品牌官网抓取与公开事实交叉验证，系统诊断 GEO 资产缺口，并输出站内和站外机会地图。"
  default_prompt: "当需要项目启动、季度复盘、竞品追赶或投放前 GEO 全景诊断时，使用 $yao-geo-panorama-audit；先抓取官网并交叉验证公开事实，完整覆盖实体、产品、内容、技术、Schema、外部信源、竞品和风险，再输出站内/站外系统方案；默认中文简体，并按白底报告版式交付 Word、PDF、带固定菜单的 HTML、Markdown。"
compatibility:
  canonical_format: "agent-skills"
  adapter_targets:
    - "openai"
    - "claude"
    - "generic"
  activation:
    mode: "manual"
    paths: []
  execution:
    context: "inline"
    shell: "bash"
  trust:
    source_tier: "local"
    remote_inline_execution: "forbid"
    remote_metadata_policy: "allow-metadata-only"
  degradation:
    openai: "metadata-adapter"
    claude: "neutral-source-plus-adapter"
    generic: "neutral-source"
