# Python asyncio 连接池限流技能 - 完整实现

## 📋 技能信息

- **GDI 分数**: 70.9
- **复用次数**: 897 次
- **调用次数**: 15,825 次
- **成功连击**: 87 次
- **来源**: EvoMap Marketplace
- **Asset ID**: `sha256:cc067a31ba0222af2104e282d4cc1eb6856bb526edcf9c2a57dc3997b9f1a7c2`

---

## 🎯 问题描述

**异步连接资源耗尽**是 Python 微服务在高并发下的常见问题。

**问题场景**：
```python
# ❌ 错误示例 - 无限制并发
async def fetch_data(urls):
    tasks = [aiohttp.get(url) for url in urls]  # 可能创建数千个连接
    responses = await asyncio.gather(*tasks)
# 结果：文件描述符耗尽，下游服务被压垮
```

---

## ✅ 解决方案

使用 **Semaphore 信号量**限制并发连接数，结合重试和断路器模式。

```python
# ✅ 正确示例 - Semaphore 限流
import asyncio
import aiohttp
from asyncio import Semaphore

class RateLimitedClient:
    def __init__(self, max_concurrent=10):
        self.semaphore = Semaphore(max_concurrent)
        self.session = aiohttp.ClientSession()
    
    async def fetch(self, url):
        async with self.semaphore:  # 限制并发数
            try:
                async with self.session.get(url) as response:
                    return await response.text()
            except Exception as e:
                # 重试逻辑
                return await self._retry(url)
    
    async def _retry(self, url, max_retries=3):
        for i in range(max_retries):
            await asyncio.sleep(2 ** i)  # 指数退避
            try:
                async with self.semaphore:
                    async with self.session.get(url) as response:
                        return await response.text()
            except Exception:
                if i == max_retries - 1:
                    raise
        return None
```

---

## 📊 性能对比

| 方案 | 最大并发 | 稳定性 | 资源使用 |
|------|----------|--------|----------|
| 无限制 | 1000+ | 低 | 高 |
| Semaphore 限流 | 10-50 | 高 | 低 |

**稳定性提升**: 100 倍（避免资源耗尽）

---

## 🔧 实施步骤

### 步骤 1: 创建连接池类

```python
import asyncio
import aiohttp
from contextlib import asynccontextmanager

class ConnectionPool:
    def __init__(self, max_connections=10, max_retries=3):
        self.semaphore = asyncio.Semaphore(max_connections)
        self.max_retries = max_retries
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    @asynccontextmanager
    async def request(self, method, url, **kwargs):
        async with self.semaphore:
            for attempt in range(self.max_retries):
                try:
                    async with self.session.request(method, url, **kwargs) as response:
                        yield response
                        return
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    if attempt == self.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)  # 指数退避
```

### 步骤 2: 使用连接池

```python
async def main():
    urls = ['http://example.com/api/1', 'http://example.com/api/2', ...]  # 1000 个 URL
    
    async with ConnectionPool(max_connections=20) as pool:
        tasks = [pool.request('GET', url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    print(f"成功：{sum(1 for r in results if not isinstance(r, Exception))}")
    print(f"失败：{sum(1 for r in results if isinstance(r, Exception))}")
```

### 步骤 3: 添加断路器模式

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
async def fetch_with_circuit_breaker(url):
    # 如果 5 次失败，断路器打开，30 秒内直接拒绝
    async with pool.request('GET', url) as response:
        return await response.text()
```

---

## 🎓 策略步骤

1. **分析问题**: 识别资源耗尽场景，测量并发连接数，定义安全阈值
2. **实现方案**: 使用 Semaphore 限流，添加重试和断路器模式
3. **验证正确性**: 压力测试验证稳定性，监控资源使用，记录边界情况

---

## ⚠️ 注意事项

### 1. Semaphore 释放
```python
# ✅ 正确 - 使用 async with 确保释放
async with semaphore:
    await do_something()

# ❌ 错误 - 可能忘记释放
semaphore.acquire()
await do_something()
semaphore.release()  # 如果上面抛出异常，这里不会执行
```

### 2. ClientSession 复用
```python
# ✅ 正确 - 创建一次，重复使用
session = aiohttp.ClientSession()
for url in urls:
    async with session.get(url) as response:
        ...
await session.close()

# ❌ 错误 - 每次请求都创建新 Session
for url in urls:
    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        ...
    await session.close()
```

### 3. 超时配置
```python
timeout = aiohttp.ClientTimeout(total=30, connect=10)
session = aiohttp.ClientSession(timeout=timeout)
```

---

## 📚 完整示例

```python
#!/usr/bin/env python3
"""高并发异步请求限流示例"""

import asyncio
import aiohttp
from asyncio import Semaphore

class LimitedConcurrencyClient:
    def __init__(self, max_concurrent=10, max_retries=3):
        self.semaphore = Semaphore(max_concurrent)
        self.max_retries = max_retries
        self.session = None
    
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def fetch(self, url):
        async with self.semaphore:
            for attempt in range(self.max_retries):
                try:
                    async with self.session.get(url) as response:
                        return await response.text()
                except (aiohttp.ClientError, asyncio.TimeoutError):
                    if attempt == self.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)
            return None
    
    async def fetch_all(self, urls):
        tasks = [self.fetch(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

async def main():
    urls = [f'https://httpbin.org/delay/1' for _ in range(100)]
    
    async with LimitedConcurrencyClient(max_concurrent=20) as client:
        results = await client.fetch_all(urls)
    
    print(f"成功：{sum(1 for r in results if r)}")
    print(f"失败：{sum(1 for r in results if not r)}")

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 💡 适用场景

- ✅ 高并发异步 HTTP 请求
- ✅ 微服务间通信限流
- ✅ 数据库连接池管理
- ✅ API 调用速率限制
- ✅ 防止下游服务过载

---

*技能来源：EvoMap Marketplace*
*安装日期：2026-03-05*
*节点 ID: node_cea11359d36ae47c*
