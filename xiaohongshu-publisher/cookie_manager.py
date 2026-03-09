#!/usr/bin/env python3
"""小红书 Cookie 管理器 - 保存和加载登录态"""

import json
import os
from pathlib import Path

DATA_DIR = Path("/app/data")
DATA_DIR.mkdir(exist_ok=True)
COOKIE_FILE = DATA_DIR / "xiaohongshu_cookies.json"


def save_cookies(context):
    """保存 Cookie 到文件"""
    cookies = context.cookies()
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"✅ Cookie 已保存：{COOKIE_FILE}")
    return True


def load_cookies():
    """从文件加载 Cookie"""
    if not COOKIE_FILE.exists():
        print("⚠️ 未找到 Cookie 文件，需要重新登录")
        return None
    
    try:
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        print(f"✅ 已加载 {len(cookies)} 个 Cookie")
        return cookies
    except Exception as e:
        print(f"❌ 加载 Cookie 失败：{e}")
        return None


def is_logged_in(cookies):
    """检查是否已登录（通过关键 Cookie 判断）"""
    if not cookies:
        return False
    
    # 小红书登录态关键 Cookie
    required_cookies = ["web_session", "a1", "webId"]
    cookie_names = {c.get("name") for c in cookies}
    
    has_session = any(name in cookie_names for name in required_cookies)
    if has_session:
        print("✅ 检测到有效登录态")
    else:
        print("⚠️ 登录态可能已过期")
    
    return has_session


def get_cookie_status():
    """返回 Cookie 状态信息"""
    if not COOKIE_FILE.exists():
        return {"exists": False, "valid": False, "message": "未找到 Cookie 文件"}
    
    cookies = load_cookies()
    if not cookies:
        return {"exists": True, "valid": False, "message": "Cookie 文件为空或损坏"}
    
    valid = is_logged_in(cookies)
    return {
        "exists": True,
        "valid": valid,
        "count": len(cookies),
        "message": "登录态有效" if valid else "登录态可能已过期"
    }
