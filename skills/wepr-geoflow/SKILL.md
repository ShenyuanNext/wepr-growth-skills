---
name: wepr-geoflow
description: 开发、运营和审计 GEOFlow，覆盖 Laravel 后端、Admin UI V3、API、CLI 0.2、内容与 AI 质检、企业知识库、系统帮助、人工发布、浏览器运营助手、PWA、托管渠道站点、数据分析、分发及独立更新工具。也适用于把已核验能力整理为客户实施方案和交付边界。任何线上访问、凭据读取、数据导入、写入、发布、升级或回滚都必须获得用户明确授权；必须先发现真实路由和部署能力，不得虚构接口、绕过鉴权、泄露密钥或直接复制网页。
---

# WEPR GEOFlow 工作台

## 路由

1. 源码任务先运行 `scripts/discover_geoflow_workspace.py <workspace>`；运行中系统的写操作前运行 `scripts/geoflow_preflight.sh "<workspace>" [config] [checks]`。可用时同时检查当前 CLI 帮助、版本和真实路由。
2. 每次只加载当前任务需要的模式：

- `development`：读取 [development-workflow.md](references/development-workflow.md) 与 [system-capability-discovery.md](references/system-capability-discovery.md)。
- `operations`：读取 [operation-boundary.md](references/operation-boundary.md)、[command-map.md](references/command-map.md) 与 [geoflow-current-capability-map.md](references/geoflow-current-capability-map.md)。
- `public_frontend`：读取 [frontend-resource-index.md](references/frontend-resource-index.md) 与 [geoflow-frontend-map.md](references/geoflow-frontend-map.md)。
- `channel_frontend`：读取 [frontend-resource-index.md](references/frontend-resource-index.md) 与 [channel-frontend-contract.md](references/channel-frontend-contract.md)。
- `legacy_migration`：读取 [legacy-template-migration.md](references/legacy-template-migration.md) 与 [legacy-skill-id-migration.md](references/legacy-skill-id-migration.md)。
- `client_delivery`：读取 [client-delivery-workflow.md](references/client-delivery-workflow.md) 与 [geoflow-current-capability-map.md](references/geoflow-current-capability-map.md)。

3. 混合任务遵循“发现 → 设计或实施 → 测试或预览 → 经批准后完成”的顺序。跨越代码、运行环境、公开发布和客户交付边界时，明确切换模式。

## 当前能力基线

- 内置 CLI 0.2.0 可管理配置、登录、目录、任务、执行记录、素材和文章，并约束 endpoint 与 credential 绑定。
- 企业知识库支持多来源资料、异步草稿、历史修订、Markdown 编辑和语义切片。
- 人工发布工作台支持文章或评论工单、身份与账号、执行人、计划时间、状态历史、重复检测和 CSV 导出，但不保存外部平台凭据。
- 站点能力覆盖版本化参考内容、企业主题、首页模块、线索表单、SEO 元数据、主题隔离预览和审查包。
- 分发能力覆盖本地站、目标站点包、GEOFlow Agent、WordPress REST 与通用 HTTP API，并保留队列、日志、远端副本和设置同步边界。
- 数据与安全能力覆盖 AI 可见性、访问分析、内容风险扫描、幂等、权限、出站请求防护、密钥脱敏和只读安全审计。
- 3.0.0 基线新增统一 Admin UI V3、系统知识与图文帮助、文章 AI 质检、托管渠道站点、浏览器运营助手、后台 PWA 和独立更新工具；具体实例仍需逐项发现并核验启用状态。
- 网站更新、完整备份和回滚在 3.0.0 中由独立更新工具承担，旧版站内执行入口不得继续作为当前操作方案。

以上只是更新时核验过的基线。任何具体实例仍以现场代码、`--help`、路由、权限和读回结果为准。

## 模式边界

每个阶段只采用一种模式。`development` 修改代码并测试；`operations` 使用受支持的运行接口；`public_frontend` 生成主题或首页配置；`channel_frontend` 处理目标站点契约；`client_delivery` 只把可验证能力转成客户可读的策略、范围和交付物，不直接改代码或发布内容。

客户需要完整营销方案时先用 `$wepr-marketing` 确定受众、定位、渠道和指标，再用本技能核验 GEOFlow 能否承接；公关与传播方案使用 `$pr-strategy-workbench`；文章和营销内容使用 `$create-marketing-content`；中文终稿使用 `$wepr-human-writing`。若需要实际录入、排程、分发或发布，必须从 `client_delivery` 切换到 `operations` 并重新确认目标与权限。

## 安全边界

- 遵循目标仓库规则并运行聚焦测试。
- 辅助脚本需 Python 3.10+ 与 Bash；运行预检还需 `curl`；实时渠道报告需 PHP CLI、可运行的项目 `artisan` 和已安装依赖。缺少依赖时只做只读发现，不宣称线上验证成功。
- 保留鉴权、CSRF、幂等、权限、读回、数据契约和密钥脱敏。
- 存储权限检查应以明确目标和状态变化为条件，避免每次请求重复扫描或修复整个存储目录；权限异常先定位路径、用户、进程和部署方式，再执行最小修复并读回验证。
- 配置与登录优先使用隐藏输入、stdin、环境变量或受限权限 profile；不要把 Token 或密码放进命令参数、文档、日志和提交。
- 区分预览、导入、同步、启用、发布、更新、回滚和删除。高风险步骤必须确认准确目标并获得明确授权。
- 人工发布工单是执行与审计工具，不代表平台授权，也不能用于批量垃圾内容、虚假身份、隐藏广告或规避平台规则。
- 浏览器运营助手只处理经管理员批准的短时设备授权和待审核草稿；最终发布仍由用户检查确认。托管渠道站点只有在泛 DNS、通配符 TLS、可信代理与反向代理配置通过后才能启用。
- 升级 3.0.0 前必须备份数据库、`.env`、上传目录和 `storage`，排空旧进程，核验迁移、前端构建、队列、调度器、实时服务及签名更新工具的兼容版本；不得只依据版本号直接执行升级。
- 交付时报告模式、证据、涉及的文件或资源、验证结果、最终状态和剩余风险。
