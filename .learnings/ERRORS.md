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

---
