# Errors Log

记录命令失败和异常。

## 格式说明

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
简要描述什么失败了

### Error
```
实际错误消息或输出
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 相关环境详情

### Suggested Fix
如果可以识别，什么可能解决这个问题

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (如果重复出现)

---
```

## 当前 Errors

## [ERR-20260310-001] config-file-not-found

**Logged**: 2026-03-10T08:52:00+08:00
**Priority**: low
**Status**: resolved
**Area**: config

### Resolution
- **Resolved**: 2026-03-10T08:52:00+08:00
- **Notes**: 使用正确路径 ~/.openclaw/openclaw.json

### Summary
尝试读取不存在的配置文件 openclaw.json

### Error
```
ENOENT: no such file or directory, access '/Users/jesson/.openclaw/config/openclaw.json'
```

### Context
- 操作：读取 OpenClaw 配置文件
- 预期路径：~/.openclaw/config/openclaw.json
- 实际路径：~/.openclaw/openclaw.json

### Suggested Fix
✅ 已解决：配置文件实际位于 `~/.openclaw/openclaw.json`，不是子目录

### Metadata
- Reproducible: no
- Related Files: ~/.openclaw/openclaw.json
- Resolution: 使用正确的路径

---

## [ERR-20260310-002] xiaohongshu-cookie-expired

**Logged**: 2026-03-10T09:24:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
小红书 MCP Cookie 过期，无法发布内容

### Error
```
failed to unmarshal cookies: json: cannot unmarshal object into Go value of type []*proto.NetworkCookie
Publish content timed out after 60000ms
```

### Context
- 操作：发布 ARRI 35 解析报告到小红书
- 容器：xiaohongshu-mcp (Docker)
- 状态：容器运行正常，但 Cookie 失效
- 用户场景：用户不在电脑旁，无法手动更新 Cookie

### Suggested Fix
✅ 已解决：
1. 用户提供最新 Cookie（通过浏览器导出）
2. 更新 ~/.agent-reach/xiaohongshu-cookies.json
3. 复制 cookies.json 到容器：docker cp ~/.agent-reach/xiaohongshu-cookies.json xiaohongshu-mcp:/app/cookies.json
4. 重启 Docker 容器
5. 发布时使用单张图片避免超时

### Resolution
- **Resolved**: 2026-03-10T09:56:00+08:00
- **PostID**: 发布成功
- **Notes**: 多张图片上传容易超时，建议只用 1 张主图或压缩图片

### Metadata
- Reproducible: yes
- Related Files: ~/.agent-reach/xiaohongshu-cookies.json
- See Also: LRN-20260310-001
- Pattern-Key: xiaohongshu.cookie-refresh

---

## [ERR-20260312-001] feishu-rate-limit

**Logged**: 2026-03-12T09:00:03+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Resolution
- **Resolved**: 2026-03-12T09:00:15+08:00
- **Notes**: 重试机制生效，后续推送（DPReview、PetaPixel 等）均成功

### Summary
飞书推送触达 API 速率限制（错误 9499: too many request）

### Error
```
❌ 发送失败：{'code': 9499, 'msg': 'too many request', 'error': {'log_id': '20260312090003DB1AC07769A0511EC22E'}}
```

### Context
- 操作：早间新闻推送（09:00 定时任务）
- 推送渠道：飞书卡片消息
- 新闻数量：2 条（MIT Technology Review）
- 日志位置：news-pusher/logs/pusher.log
- 首次出现：2026-03-12（之前推送正常）

### Suggested Fix
1. **添加重试机制**：遇到 9499 错误时，等待 60 秒后重试
2. **添加请求间隔**：多条新闻之间增加 2-5 秒延迟
3. **检查应用配额**：确认飞书应用 API 调用配额
4. **监控频率**：如果频繁出现，考虑减少推送频率或合并消息

### Metadata
- Reproducible: unknown
- Related Files: news-pusher/pusher_feishu_app.py, news-pusher/config.yaml
- See Also: LRN-20260310-002 (小红书发布流程)
- Pattern-Key: feishu.rate-limit-handling

---
