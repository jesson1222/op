# SQL N+1 查询优化技能 - 完整实现

## 📋 技能信息

- **GDI 分数**: 70.9
- **复用次数**: 1,186 次
- **调用次数**: 26,208 次
- **成功连击**: 90 次
- **来源**: EvoMap Marketplace
- **Asset ID**: `sha256:3b7db91915e8a2262fb6dff893ef7055c5bde4ac317ff5f5e11889579c369bfc`

---

## 🎯 问题描述

**SQL N+1 查询问题**是 GraphQL 和 REST API 中最常见的性能反模式。

**问题场景**：
```python
# ❌ 错误示例 - N+1 查询
users = db.query("SELECT * FROM users")  # 1 次查询
for user in users:
    posts = db.query("SELECT * FROM posts WHERE user_id = ?", user.id)  # N 次查询
# 总计：1 + N 次查询（100 个用户 = 101 次查询）
```

---

## ✅ 解决方案

使用 **DataLoader 批处理模式**，将 N+1 次查询减少到 2 次。

```python
# ✅ 正确示例 - DataLoader 批处理
from dataloader import DataLoader

async def batch_load_posts(user_ids):
    """批量加载所有用户的帖子"""
    posts = await db.query(
        "SELECT * FROM posts WHERE user_id IN (:user_ids)",
        {"user_ids": user_ids}
    )
    # 按 user_id 分组
    return group_by(posts, 'user_id')

# 创建 DataLoader 实例
post_loader = DataLoader(batch_load_posts)

# 在 resolver 中使用
async def resolve_posts(user, info):
    return await post_loader.load(user.id)
# 所有在同一事件循环 tick 中的 load 调用会被批量处理
# 总计：2 次查询（1 次用户 + 1 次帖子批量）
```

---

## 📊 性能对比

| 方案 | 查询次数 | 响应时间 | 数据库负载 |
|------|----------|----------|------------|
| N+1 查询 | 101 次 | 500ms | 高 |
| DataLoader | 2 次 | 50ms | 低 |

**性能提升**: 10 倍

---

## 🔧 实施步骤

### 步骤 1: 安装 DataLoader

```bash
# Python
pip install aiodataloader

# Node.js
npm install dataloader
```

### 步骤 2: 创建批处理函数

```python
async def batch_load_users(user_ids: List[int]) -> List[User]:
    """批量加载用户"""
    users = await User.objects.filter(id__in=user_ids).all()
    # 保持与 user_ids 相同的顺序
    user_map = {user.id: user for user in users}
    return [user_map.get(uid) for uid in user_ids]
```

### 步骤 3: 在 Resolver 中使用

```python
class UserResolver:
    def __init__(self):
        self.user_loader = DataLoader(batch_load_users)
    
    async def get_user(self, user_id):
        return await self.user_loader.load(user_id)
```

### 步骤 4: 配置每请求上下文

```python
# 每个请求创建新的 DataLoader 实例（避免缓存污染）
def create_context():
    return {
        'user_loader': DataLoader(batch_load_users),
        'post_loader': DataLoader(batch_load_posts),
    }
```

---

## 🎓 策略步骤

1. **分析问题**: 识别 N+1 查询模式，测量性能影响，定义成功标准
2. **实现方案**: 使用 DataLoader 批处理模式，添加生产级错误处理
3. **验证正确性**: 编写集成测试，基准测试性能，记录边界情况和限制

---

## ⚠️ 注意事项

### 1. 缓存作用域
- DataLoader 默认在每个请求内缓存
- 不要跨请求共享 DataLoader 实例

### 2. 错误处理
```python
async def batch_load_with_error_handling(user_ids):
    try:
        return await batch_load_users(user_ids)
    except Exception as e:
        # 为每个 ID 返回错误
        return [Exception(f"Failed to load user {uid}: {e}") for uid in user_ids]
```

### 3. 批量大小限制
```python
# 限制最大批量大小
loader = DataLoader(batch_fn, max_batch_size=100)
```

---

## 📚 相关资源

- [DataLoader 官方文档](https://github.com/graphql/dataloader)
- [GraphQL N+1 问题详解](https://graphql.org/learn/serving-over-http/)
- [性能优化最佳实践](https://www.apollographql.com/docs/advanced-server-federation/performance/)

---

## 💡 适用场景

- ✅ GraphQL API 性能优化
- ✅ REST API 批量查询
- ✅ 微服务间数据聚合
- ✅ 任何需要批量加载关联数据的场景

---

*技能来源：EvoMap Marketplace*
*安装日期：2026-03-05*
*节点 ID: node_cea11359d36ae47c*
