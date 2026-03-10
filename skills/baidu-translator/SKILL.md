# 🔤 百度翻译技能

## 描述

使用百度翻译 API 进行英文到中文的翻译，适用于新闻标题、文章摘要等短文本翻译。国内访问稳定，免费额度充足。

## 触发条件

用户需要翻译英文内容，尤其是：
- RSS 新闻标题翻译
- 文章摘要翻译
- 短文本英译中

## 配置步骤

### 1. 申请百度翻译 API（5 分钟）

1. 访问 https://fanyi-api.baidu.com/
2. 点击右上角「管理控制台」
3. 登录百度账号（没有就注册）
4. 完成**实名认证**（需要手机号）
5. 点击「开通服务」→ 选择「通用文本翻译」（标准版）
6. 填写应用信息（名称随意）
7. 获取 APP ID 和密钥

### 2. 配置 YAML

```yaml
translate:
  enabled: true
  baidu_app_id: "你的 APP ID"
  baidu_app_key: "你的密钥"
```

### 3. 测试翻译

```python
from pusher_feishu_app import Translator
t = Translator('APP_ID', 'APP_KEY')
result = t.translate('How AI is changing the world', 'en', 'zh')
print(result)  # 人工智能如何改变世界
```

## 代码实现

### Translator 类

```python
class Translator:
    """翻译器 - 使用百度翻译 API（国内可访问）"""
    
    def __init__(self, app_id: str = None, app_key: str = None):
        self.cache = {}  # 翻译缓存
        self.api_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
        self.app_id = app_id
        self.app_key = app_key
        self.use_baidu = bool(app_id and app_key)
    
    def translate(self, text: str, source: str = "en", target: str = "zh") -> str:
        """翻译文本"""
        if not text or len(text.strip()) < 2:
            return text
        
        # 检查缓存
        cache_key = f"{source}->{target}:{text[:100]}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 检测是否已经是中文
        if self._is_chinese(text):
            return text
        
        # 未配置百度翻译，返回原文
        if not self.use_baidu:
            return text
        
        import hashlib
        import random
        
        try:
            # 百度翻译 API v1
            salt = random.randint(32768, 65536)
            sign = hashlib.md5(f"{self.app_id}{text}{salt}{self.app_key}".encode('utf-8')).hexdigest()
            
            params = {
                "q": text[:2000],
                "from": source,
                "to": target,
                "appid": self.app_id,
                "salt": str(salt),
                "sign": sign
            }
            
            response = requests.post(self.api_url, data=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # 检查错误码
                if 'error_code' in result:
                    error_code = result.get('error_code', '')
                    error_msg = result.get('error_msg', '')
                    print(f"⚠️ 百度翻译错误 {error_code}: {error_msg}")
                    
                    # 52003 = 未授权，需要实名认证或开通服务
                    if error_code == '52003':
                        print(f"💡 请在百度翻译控制台完成实名认证并开通【通用翻译 API】服务")
                    return text
                
                # 提取翻译结果
                if 'trans_result' in result:
                    translated_parts = [item['dst'] for item in result['trans_result'] if 'dst' in item]
                    translated = ''.join(translated_parts)
                    
                    if translated:
                        self.cache[cache_key] = translated
                        return translated
            
            return text
            
        except Exception as e:
            print(f"⚠️ 翻译异常 ({type(e).__name__}): {e}")
            return text
    
    def _is_chinese(self, text: str) -> bool:
        """检测文本是否包含中文"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
```

## 错误处理

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 52003 | UNAUTHORIZED USER | 未完成实名认证或未开通服务 |
| 54001 | Invalid Sign | 密钥错误，检查 APP ID 和密钥是否匹配 |
| 54003 | Invalid Salt | salt 参数格式错误 |
| 54004 | Invalid Sign | 签名计算错误 |

## 免费额度

- **QPS**：1 次/秒
- **月额度**：200 万字符
- **实际使用**：每次推送约 500-1000 字符，每天 2 次，每月约 6 万字符

✅ 免费额度完全够用！

## 最佳实践

1. **缓存翻译结果**：避免重复翻译相同内容
2. **批量翻译**：一次性翻译多条，减少 API 调用
3. **失败降级**：翻译失败时返回原文，不影响流程
4. **中文检测**：已经是中文的内容跳过翻译

## 相关文件

- 配置：`news-pusher/config_feishu_app.yaml`
- 脚本：`news-pusher/pusher_feishu_app.py`
- 指南：`news-pusher/TRANSLATE_SETUP.md`

## 历史

- 2026-03-10：从 Google 翻译迁移到百度翻译（Google API 在国内无法访问）
- 2026-03-10：完成实名认证和 API 配置，测试通过
