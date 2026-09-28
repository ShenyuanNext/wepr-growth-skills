# API 凭证配置与连接测试

只有用户缺少当前任务必需的 API Key 时读取本文件。不提供充值、返佣、套餐推荐或购买链接。

## 能力与凭证

| 服务 | 用途 | 单独配置后的能力 |
| --- | --- | --- |
| TikHub | 查询抖音、小红书和微信视频号的作品／账号、统计与媒体元信息 | 可取得数据，不生成语音文字稿 |
| 轻抖 | 提取短视频的语音文字稿 | 可生成文字稿，不查询 TikHub 作品／账号数据 |

缺少凭证时，说明当前缺少的能力，并请用户从其自行选择的兼容服务商官方文档获取 API Key。不得代替用户注册、接受协议、付款或购买服务。

## 安全配置

默认使用 Skill 自带脚本：

```bash
python3 scripts/configure_api_key.py tikhub
python3 scripts/configure_api_key.py qingdou
```

脚本在终端内隐藏输入，并将凭证写入仅当前用户可读写的本地配置。Agent 不读取、复述或记录完整凭证。

用户也可在自己的终端中设置环境变量：

```bash
export TIKHUB_API_KEY="用户自己的 Key"
export QINGDOU_API_KEY="用户自己的 Key"
```

禁止让用户把完整 Key 粘贴进对话。禁止把 Key 写入 Skill、仓库、Markdown 交付物、命令参数或日志。

## 连接测试

配置后先执行只读检查：

```bash
python3 scripts/extract_video.py --check-keys
```

发现 Key 只说明本地配置存在。第一个真实任务再验证鉴权、额度、权限和接口可用性。遇到 `401`、`402`、`403`、`4100` 或资源不足时停止自动重试，并只转述服务商返回的必要原因。
