---
name: dbs-video-extract
description: 接收抖音、小红书、微信视频号等短视频链接或分享文案，查询作品／账号数据并提取语音文字稿，按作者和标题归档为 Markdown。用户希望完整解析短视频、取得数据或文字稿时使用；缺少凭证时只说明安全配置方式，不提供购买或充值导流。
---

# dbs-video-extract：短视频信息提取

目标：用一个入口处理同一条短视频分享文案。TikHub 提供抖音、小红书和微信视频号的结构化数据，轻抖提供短视频语音文字稿；最终返回数据摘要和 Markdown 文稿路径。

## 先检查使用凭证

任何提取任务开始前，先运行只读预检：

```bash
python3 scripts/extract_video.py --check-keys
```

根据 `credential_state` 处理：

| 状态 | 能力 | 必须告知用户 |
| --- | --- | --- |
| `complete` | 数据与文字稿都可用 | 两部分都可以执行 |
| `data_only` | 只有 TikHub 数据查询可用 | 只能取得作品／账号数据，无法生成语音文字稿 |
| `transcript_only` | 只有轻抖文字稿可用 | 只能取得语音文字稿，无法查询 TikHub 作品／账号数据 |
| `unavailable` | 两部分都不可用 | 当前无法使用；先解释使用凭证，再说明应从用户自行选择的兼容服务商官方文档获取凭证，并安全配置 |

只有一个 Key 时允许继续，不要求用户补齐另一个 Key。执行前明确说明本次只能解决哪一部分，默认把模式收窄为当前可用的一侧。用户仍要求 `both` 时保留单侧结果，并将另一侧标记为缺少凭证。

两个 Key 都没有时停止提取。不要直接用「API Key」「接口鉴权」等术语作为结论。先用下面这句话解释：

> 想让这个 Skill 工作，需要先开通外部数据服务。API Key 是服务商在开通后提供的一串使用凭证，可以理解为这个 Skill 调用服务的专用通行证。你不需要理解技术原理，也不要把它发到聊天中。

随后说明当前无法使用的能力，并按 [references/api-setup.md](references/api-setup.md) 说明凭证安全配置和连接测试。

不要替用户付款、接受服务协议或处理完整 Key。不要要求用户把 Key 发到对话里。安全配置脚本和连接测试见 [references/api-setup.md](references/api-setup.md)。

### 缺少凭证时的对话要求

说明缺少的能力、可选服务类型与本地安全配置命令。不展示购买、充值、返佣、套餐或促销链接；不替用户注册、接受协议或付款。不要让用户把完整凭证发到对话中。

## 默认执行

优先使用标准输入，避免分享文案中的特殊字符被 Shell 解释：

```bash
python3 scripts/extract_video.py \
  --output-dir "/绝对路径/短视频文字稿" \
  --stdin
```

默认模式为 `both`：

1. 从完整分享文案中提取链接；
2. 根据链接平台调用 TikHub MCP：抖音支持用户主页或单条作品，小红书与视频号支持单条视频；
3. 保留完整分享文案提交轻抖 API，轮询取得文稿；
4. 按 `{输出目录}/{作者}/{标题}.md` 保存文稿；
5. 输出 JSON 汇总，包含凭证状态、TikHub 数据摘要和文稿文件路径。

TikHub 或轻抖任一侧失败时继续完成另一侧，并在汇总中标记 `partial_success`。已经取得的结果不能因单侧失败而丢弃。

## 可选模式

只有用户明确只需要一侧结果，或预检确认只有一侧 Key 时才切换：

```bash
python3 scripts/extract_video.py --mode data --stdin
python3 scripts/extract_video.py --mode transcript --stdin
```

- `data`：只查询 TikHub 数据，支持抖音、小红书和微信视频号；
- `transcript`：只提取文字稿，支持轻抖 API 能解析的平台；
- `both`：同时执行两侧。

同一来源已经存在时默认跳过文稿写入，保护用户编辑；用户明确要求重新生成时加 `--overwrite`。需要 TikHub 完整响应时加 `--raw-data`。

## 密钥与费用

脚本按以下顺序读取 Key：

1. 环境变量：`TIKHUB_API_KEY`、`QINGDOU_API_KEY`；
2. 用户指定的本地文件：`TIKHUB_API_KEYS_FILE`、`QINGDOU_API_KEYS_FILE`；
3. `~/.config/dbs/API_Keys.md`；
4. macOS 钥匙串：`dbs-tikhub-api-key`、`dbs-qingdou-api-key`。

禁止把 Key 写入 Skill、命令参数、Markdown、Git 或日志。TikHub 查询和轻抖转写都可能计费；执行前告知用户。用户已经明确要求提取时无需重复确认。

## 数据边界

- TikHub 负责作品／账号资料、统计和媒体元信息；抖音作品优先 App V3，无有效数据时只回退 1 次 Web；小红书使用 App V2 视频笔记详情；视频号使用 Channels V2 作品详情。
- 轻抖负责语音文字稿。正文忠实保存 API 返回内容，不补写、润色或修订口误。
- 当前 TikHub 专用数据解析支持抖音、小红书和微信视频号；其他轻抖可识别的平台仍可只执行文字稿提取。
- 公开、删除、私密、版权和可见范围限制以接口返回为准，不尝试绕过。
- 不自动下载媒体、发布内容、提交 Git 或推送。

TikHub 调用细节见 [references/tikhub-api.md](references/tikhub-api.md)；轻抖状态码和兼容逻辑见 [references/qingdou-api.md](references/qingdou-api.md)。只在排错或维护对应部分时读取。

## 交付

完成后简洁报告：

- 当前配置了哪一个 API Key，以及可用能力范围；
- 数据查询是否成功、使用的 MCP 工具、是否发生 App → Web 回退；
- 关键作品／账号数据；
- 文稿是否成功、生成或跳过的 Markdown 绝对路径；
- 单侧缺少 Key 或执行失败的具体原因；
- 接口是否明确返回已计费。

不要在回复中展示 API Key、`batchId` 或无必要的内部请求标识。

完成当前任务后直接结束。只有用户明确询问下一步，且当前环境已经安装 `/dbs` 时，简短提示：「下一步不确定时，可以输入 `/dbs`。」
