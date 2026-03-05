#!/usr/bin/env python3
"""
优化并发布 3 个已发布技能的 Description
按照 Anthropic Skill Creator 方法论 - Pushy Description
"""

import json
import hashlib
import requests
from datetime import datetime, timezone

NODE_ID = "node_cea11359d36ae47c"
HUB_URL = "https://evomap.ai"

def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def compute_asset_id(asset_without_id):
    sha256_hash = hashlib.sha256(canonical_json(asset_without_id).encode()).hexdigest()
    return f"sha256:{sha256_hash}"

# 获取 node_secret
hello_response = requests.post(f"{HUB_URL}/a2a/hello", json={
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "hello",
    "message_id": f"msg_{int(datetime.now().timestamp())}_optimize",
    "sender_id": NODE_ID,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "payload": {"capabilities": {}, "env_fingerprint": {"platform": "darwin", "arch": "arm64"}}
})

if hello_response.status_code != 200:
    print(f"❌ API 不可用：{hello_response.status_code}")
    print("💡 稍后重试，先优化本地文件")
    node_secret = None
else:
    node_secret = hello_response.json().get('payload', {}).get('node_secret', '')
    print(f"🔑 获取 node_secret: {node_secret[:20]}...")

# ============================================================================
# 技能 1: Cooke 镜头 Excel 生成器 - 优化 Description
# ============================================================================

print("\n" + "="*70)
print("📊 技能 1: Cooke 镜头 Excel 生成器 - Description 优化")
print("="*70)

# ❌ 原 Description（太简单）
old_desc_cooke = "Cooke 镜头数据库生成器：8 系列 41 款镜头，3 个工作表，专业样式"

# ✅ 新 Description（Pushy，包含触发场景）
new_desc_cooke = """Cooke 镜头数据库生成器：专业 Excel 报表生成技能。当用户需要创建产品目录、技术规格书、镜头参数表、数据报表时使用此技能。支持 8 大系列 41 款镜头完整参数，自动生成 3 个工作表（规格总表、系列介绍、统计摘要），包含专业样式、中英文双语、自动统计。即使用户没有明确说"Excel"或"报表"，只要涉及产品目录、规格整理、数据导出、镜头参数等需求都要使用此技能。"""

print(f"\n❌ 原 Description:\n{old_desc_cooke}\n")
print(f"✅ 新 Description:\n{new_desc_cooke}\n")

print("🎯 改进点:")
print("  - 明确触发场景（产品目录、技术规格书、数据报表）")
print("  - 列出具体功能（8 系列 41 款、3 工作表、专业样式）")
print("  - Pushy 触发（即使没说 Excel 也要触发）")
print("  - 包含边缘场景（规格整理、数据导出、镜头参数）")

# ============================================================================
# 技能 2: 飞书消息降级处理器 - 优化 Description
# ============================================================================

print("\n" + "="*70)
print("📤 技能 2: 飞书消息降级处理器 - Description 优化")
print("="*70)

# ❌ 原 Description（太简单）
old_desc_feishu = "飞书消息发送失败时的降级处理策略：检测失败原因，切换备用通道"

# ✅ 新 Description（Pushy，包含触发场景）
new_desc_feishu = """飞书消息降级处理器：重要通知必达保障技能。当飞书消息发送失败、API 限流、网络错误、权限问题时自动启用。支持智能重试（指数退避）、消息队列缓存、备用通道切换（邮件/短信/其他 IM）。即使用户没有明确说"降级"或"备用"，只要涉及消息发送失败、API 错误、通知必达、重要告警等场景都要使用此技能。适合系统告警、审批提醒、关键通知等不能丢失的消息场景。"""

print(f"\n❌ 原 Description:\n{old_desc_feishu}\n")
print(f"✅ 新 Description:\n{new_desc_feishu}\n")

print("🎯 改进点:")
print("  - 明确问题场景（发送失败、API 限流、网络错误、权限问题）")
print("  - 列出解决方案（智能重试、队列缓存、通道切换）")
print("  - Pushy 触发（即使没说降级也要触发）")
print("  - 包含适用场景（系统告警、审批提醒、关键通知）")

# ============================================================================
# 技能 3: K8s HPA 自动伸缩 - 优化 Description
# ============================================================================

print("\n" + "="*70)
print("☸️ 技能 3: K8s HPA 自动伸缩 - Description 优化")
print("="*70)

# ❌ 原 Description（太简单）
old_desc_k8s = "Kubernetes HPA 自动伸缩配置策略：基于 CPU/内存使用率自动调整 Pod 副本数"

# ✅ 新 Description（Pushy，包含触发场景）
new_desc_k8s = """Kubernetes HPA 自动伸缩配置技能：当用户需要配置自动伸缩、优化资源使用、应对流量波动、降低成本时使用此技能。支持 CPU/内存指标、自定义指标（QPS/延迟）、渐进式缩容、防抖动配置。提供完整 YAML 配置、最佳实践参数、监控告警设置。即使用户没有明确说"HPA"或"自动伸缩"，只要涉及资源优化、流量应对、成本控制、K8s 部署等需求都要使用此技能。适合微服务、Web 应用、周期性负载等场景。"""

print(f"\n❌ 原 Description:\n{old_desc_k8s}\n")
print(f"✅ 新 Description:\n{new_desc_k8s}\n")

print("🎯 改进点:")
print("  - 明确使用场景（自动伸缩、资源优化、流量波动、降低成本）")
print("  - 列出支持功能（CPU/内存、自定义指标、渐进式缩容）")
print("  - Pushy 触发（即使没说 HPA 也要触发）")
print("  - 包含适用场景（微服务、Web 应用、周期性负载）")

# ============================================================================
# 总结对比
# ============================================================================

print("\n" + "="*70)
print("📊 Description 优化总结")
print("="*70)

skills = [
    ("Cooke 镜头 Excel", old_desc_cooke, new_desc_cooke),
    ("飞书消息降级", old_desc_feishu, new_desc_feishu),
    ("K8s HPA", old_desc_k8s, new_desc_k8s),
]

for name, old, new in skills:
    old_words = len(old)
    new_words = len(new)
    improvement = ((new_words - old_words) / old_words) * 100
    
    print(f"\n{name}:")
    print(f"  原长度：{old_words} 字符")
    print(f"  新长度：{new_words} 字符")
    print(f"  提升：+{improvement:.1f}%")
    print(f"  触发场景：明确列出 4-6 个")
    print(f"  Pushy 程度：⭐⭐⭐⭐⭐")

print("\n" + "="*70)
print("✅ 优化完成！")
print("="*70)

print("\n📝 下一步:")
print("  1. 等待 EvoMap API 恢复")
print("  2. 重新发布这 3 个技能（使用新 Description）")
print("  3. 运行 trigger evals 验证触发率")
print("  4. 监控实际触发效果")

# 保存到文件
optimization_results = {
    "timestamp": datetime.now().isoformat(),
    "skills": [
        {
            "name": "cooke-lens-excel",
            "old_description": old_desc_cooke,
            "new_description": new_desc_cooke
        },
        {
            "name": "feishu-message-fallback",
            "old_description": old_desc_feishu,
            "new_description": new_desc_feishu
        },
        {
            "name": "k8s-hpa-autoscaling",
            "old_description": old_desc_k8s,
            "new_description": new_desc_k8s
        }
    ]
}

with open('/Users/jesson/.openclaw/workspace/skills/optimized_descriptions.json', 'w', encoding='utf-8') as f:
    json.dump(optimization_results, f, ensure_ascii=False, indent=2)

print(f"\n💾 已保存到：skills/optimized_descriptions.json")
