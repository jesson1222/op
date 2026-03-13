#!/usr/bin/env node
/**
 * iFlow API Key 自动获取脚本
 * 使用 Playwright 自动登录并提取 API Key
 */

import { chromium } from 'playwright';
import { writeFile } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCREENSHOT_DIR = '/Users/jesson/.openclaw/workspace/screenshots';
const LOG_FILE = '/Users/jesson/.openclaw/workspace/logs/iflow-auto-key.log';

// 颜色
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  const timestamp = new Date().toLocaleString('zh-CN');
  console.log(`${colors[color]}[${timestamp}] ${message}${colors.reset}`);
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function getIfloApiKey() {
  console.log('');
  log('🚀 启动 iFlow API Key 自动获取...', 'cyan');
  console.log('');
  
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--window-size=1280,800', '--disable-blink-features=AutomationControlled'],
    ignoreDefaultArgs: ['--enable-automation']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    bypassCSP: true
  });
  
  const page = await context.newPage();
  
  try {
    log('📱 访问 iFlow 设置页面...', 'blue');
    
    // 注入反检测脚本
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      });
    });
    
    await page.goto('https://iflow.cn/?open=setting', { 
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });
    
    // 等待页面稳定
    await sleep(3000);
    
    await sleep(2000);
    await page.screenshot({ path: join(SCREENSHOT_DIR, 'iflow-page.png') });
    log('📸 页面截图已保存', 'green');
    
    // 检测是否需要登录
    const needsLogin = await page.evaluate(() => {
      const loginButtons = document.querySelectorAll('button, a');
      for (const btn of loginButtons) {
        const text = btn.textContent.toLowerCase();
        if (text.includes('登录') || text.includes('login') || text.includes('sign in')) {
          return true;
        }
      }
      return false;
    });
    
    if (needsLogin) {
      log('⚠️  检测到需要登录...', 'yellow');
      console.log('');
      console.log('   请在打开的浏览器窗口中完成登录：');
      console.log('   1. 使用微信或手机号登录');
      console.log('   2. 登录成功后，页面会自动跳转到设置页');
      console.log('   3. 等待 10 秒后继续...');
      console.log('');
      
      // 等待用户登录（最长 2 分钟）
      for (let i = 0; i < 12; i++) {
        await sleep(10000);
        log(`⏳ 等待登录... (${(i + 1) * 10}秒)`, 'blue');
        
        const stillNeedsLogin = await page.evaluate(() => {
          const loginButtons = document.querySelectorAll('button, a');
          for (const btn of loginButtons) {
            const text = btn.textContent.toLowerCase();
            if (text.includes('登录') || text.includes('login')) {
              return true;
            }
          }
          return false;
        });
        
        if (!stillNeedsLogin) {
          log('✅ 检测到登录成功！', 'green');
          break;
        }
      }
    }
    
    // 查找 API Key
    log('🔍 查找 API Key...', 'blue');
    await sleep(3000);
    
    const apiKey = await page.evaluate(() => {
      // 尝试多种选择器
      const selectors = [
        'input[placeholder*="API"]',
        'input[placeholder*="api"]',
        'input[placeholder*="Key"]',
        'input[placeholder*="key"]',
        'input[placeholder*="密钥"]',
        'input[value^="sk-"]',
        'code',
        '.api-key',
        '.api_key',
        '[class*="api-key"]',
        '[class*="apikey"]',
        '[class*="api_key"]',
        'input[type="text"]',
        'input[type="password"]',
        '[data-testid*="api"]',
        '[data-testid*="key"]'
      ];
      
      for (const selector of selectors) {
        try {
          const elements = document.querySelectorAll(selector);
          for (const element of elements) {
            const value = element.value || element.textContent || '';
            if (value.includes('sk-') && value.length > 35) {
              return value.trim();
            }
          }
        } catch (e) {
          // 忽略错误
        }
      }
      
      // 尝试查找包含 sk- 的任何文本
      const allText = document.body.innerText;
      const matches = allText.match(/sk-[a-zA-Z0-9]{32}/g);
      if (matches && matches.length > 0) {
        return matches[0];
      }
      
      return null;
    });
    
    if (apiKey && apiKey.startsWith('sk-')) {
      log('✅ 成功获取 API Key!', 'green');
      console.log('');
      console.log(`   Key: ${apiKey.substring(0, 15)}...${apiKey.substring(apiKey.length - 8)}`);
      console.log('');
      
      // 保存到临时文件
      const tempFile = '/tmp/iflow-api-key.txt';
      await writeFile(tempFile, apiKey);
      log(`📝 Key 已保存到：${tempFile}`, 'green');
      console.log('');
      
      // 自动调用更新脚本
      console.log('   是否自动更新配置？(y/n): ');
      
      // 由于 Node.js 读取 stdin 复杂，我们直接给出命令
      console.log('');
      console.log('   请运行以下命令更新配置：');
      console.log('');
      console.log(`   ${colors.green}~/.openclaw/workspace/scripts/iflow-update-key.sh ${apiKey}${colors.reset}`);
      console.log('');
      
      await browser.close();
      return apiKey;
    } else {
      log('⚠️  未能自动提取 API Key', 'yellow');
      console.log('');
      console.log('   请手动复制 API Key，然后运行：');
      console.log('');
      console.log('   ~/.openclaw/workspace/scripts/iflow-update-key.sh sk-你的 key');
      console.log('');
      
      await browser.close();
      return null;
    }
  } catch (error) {
    log(`❌ 错误：${error.message}`, 'red');
    await browser.close();
    throw error;
  }
}

// 主程序
getIfloApiKey()
  .then(key => {
    if (key) {
      console.log('');
      log('🎉 完成！', 'green');
      process.exit(0);
    } else {
      process.exit(1);
    }
  })
  .catch(err => {
    console.error(err);
    process.exit(1);
  });
