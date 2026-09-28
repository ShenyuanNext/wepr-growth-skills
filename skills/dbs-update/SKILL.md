---
name: dbs-update
description: 更新 ShenyuanNext/wepr-growth-skills 中的全部公开 Skill，并保留用户存档和其他本地 Skill。用户明确要求更新或升级该技能集时使用。
---

# dbs-update：更新 ShenyuanNext/wepr-growth-skills

只在用户明确要求更新时执行；需要 Shell 或网络权限时，由用户在宿主的权限窗口中决定。

## 更新范围

- 只更新 `ShenyuanNext/wepr-growth-skills`。
- 保留用户在 `~/.dbs/` 中的存档、报告和决策记录。
- 不更新用户安装的其他 Skill。
- 不创建后台任务、定时任务或 Agent Hook。

## 执行步骤

1. 运行以下命令，同步官方 dbskill 的全部正式 Skill 到已支持的 Agent：

   ```bash
   npx -y skills add ShenyuanNext/wepr-growth-skills -g --all
   ```

2. 命令成功后记录本次更新时间，避免当前对话仍加载旧 Skill 时重复提醒：

   ```bash
   mkdir -p "$HOME/.dbs" && date +%s > "$HOME/.dbs/update_check_at"
   ```

3. 根据安装命令的退出状态确认是否完成。命令成功时告诉用户更新已完成，并提醒用户新建一次对话后再使用新能力。

4. 命令失败时，用一句话说明失败原因和下一步需要用户处理的权限或网络问题。不要把完整终端日志直接贴给用户，除非用户要求。

## 回复格式

成功：

> dbskill 已更新完成。当前对话如果还没有读取到新能力，新建一次对话后即可使用。

失败：

> dbskill 没有更新完成：{简短原因}。处理完 {权限或网络问题} 后，再说一次「更新 dbskill」。

## 边界

- 用户只问版本、更新内容或是否需要更新时，先回答问题，不执行命令。
- 用户明确要求检查更新且希望实际同步时，按本 Skill 更新。
- 不使用 `npx skills update`，该命令可能更新用户安装的其他 Skill。

---

完成当前任务后直接结束。只有用户明确询问下一步，且当前环境已经安装 `/dbs` 时，简短提示：「下一步不确定时，可以输入 `/dbs`。」
