#!/bin/bash
# iFlow API Key 自动刷新脚本
# 使用 Playwright 自动登录并获取新 Key

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 配置
IFLOW_URL="https://iflow.cn/?open=setting"
STATE_FILE="$HOME/.openclaw/workspace/.iflow-key-state.json"
SCREENSHOT_DIR="$HOME/.openclaw/workspace/screenshots"
LOG_FILE="$HOME/.openclaw/workspace/logs/iflow-auto-refresh.log"

# 确保目录存在
mkdir -p "$SCREENSHOT_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🚀 开始自动获取 iFlow API Key..."

# 检查 Playwright
if ! command -v node &> /dev/null; then
    log "${RED}❌ 需要 Node.js${NC}"
    exit 1
fi

# 创建自动化脚本
cat > /tmp/iflow-autofill.mjs << 'MJS'
import { chromium } from 'playwright';

async function getIfloApiKey() {
    const browser = await chromium.launch({ 
        headless: false,
        args: ['--window-size=1280,800']
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 800 }
    });
    
    const page = await context.newPage();
    
    console.log('📱 访问 iFlow 设置页面...');
    await page.goto('https://iflow.cn/?open=setting', { 
        waitUntil: 'networkidle',
        timeout: 30000
    });
    
    // 截图保存当前状态
    await page.screenshot({ path: '/Users/jesson/.openclaw/workspace/screenshots/iflow-before.png' });
    
    console.log('⏳ 等待用户手动登录并生成 API Key...');
    console.log('💡 提示：请在打开的浏览器窗口中：');
    console.log('   1. 登录账号（如未登录）');
    console.log('   2. 找到 "API Key" 或 "密钥管理"');
    console.log('   3. 点击 "生成" 或 "复制" 按钮');
    console.log('   4. 完成后在此终端按回车');
    
    // 等待用户操作
    await new Promise(resolve => {
        const readline = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        readline.question('✅ 完成后按回车继续...', () => {
            readline.close();
            resolve();
        });
    });
    
    // 尝试自动提取 API Key
    console.log('🔍 尝试自动提取 API Key...');
    
    try {
        // 查找 API Key 输入框或显示区域
        const apiKey = await page.evaluate(() => {
            // 尝试多种选择器
            const selectors = [
                'input[placeholder*="API"]',
                'input[placeholder*="api"]',
                'input[placeholder*="Key"]',
                'input[placeholder*="key"]',
                'input[placeholder*="密钥"]',
                'code',
                '.api-key',
                '.api_key',
                '[class*="api-key"]',
                '[class*="apikey"]',
                'input[type="text"]',
                'input[value^="sk-"]'
            ];
            
            for (const selector of selectors) {
                const element = document.querySelector(selector);
                if (element) {
                    const value = element.value || element.textContent;
                    if (value && value.includes('sk-')) {
                        return value.trim();
                    }
                }
            }
            
            return null;
        });
        
        if (apiKey && apiKey.startsWith('sk-')) {
            console.log('✅ 自动获取到 API Key:', apiKey);
            console.log('API_KEY:' + apiKey);
        } else {
            console.log('⚠️  未能自动提取 API Key');
            console.log('💡 请手动复制后运行更新脚本');
            console.log('MANUAL_COPY_REQUIRED');
        }
    } catch (e) {
        console.log('⚠️  提取失败:', e.message);
    }
    
    // 再次截图
    await page.screenshot({ path: '/Users/jesson/.openclaw/workspace/screenshots/iflow-after.png' });
    
    await browser.close();
}

getIfloApiKey().catch(console.error);
MJS

echo ""
echo -e "${YELLOW}🌐 即将打开浏览器...${NC}"
echo ""

# 运行自动化脚本
cd /tmp
node iflow-autofill.mjs 2>&1 | tee -a "$LOG_FILE"

echo ""
echo -e "${GREEN}✅ 自动获取流程完成${NC}"
echo ""
echo "📸 截图已保存到：$SCREENSHOT_DIR/"
echo ""
echo "📋 下一步："
echo "   如果自动获取成功，运行："
echo "   ~/.openclaw/workspace/scripts/iflow-update-key.sh <获取到的 Key>"
echo ""
echo "   如果需要手动复制，请："
echo "   1. 从浏览器中复制 API Key"
echo "   2. 运行更新脚本"
