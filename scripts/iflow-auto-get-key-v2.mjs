#!/usr/bin/env node
/**
 * iFlow API Key 自动获取脚本 v2
 * 改进版：尝试点击复制按钮
 */

import { chromium } from 'playwright';
import { writeFile, readFile } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';
import { promisify } from 'util';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCREENSHOT_DIR = '/Users/jesson/.openclaw/workspace/screenshots';
const LOG_FILE = '/Users/jesson/.openclaw/workspace/logs/iflow-auto-key.log';
const execAsync = promisify(exec);

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
  log('🚀 启动 iFlow API Key 自动获取 v2...', 'cyan');
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
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      });
    });
    
    log('📱 访问 iFlow 设置页面...', 'blue');
    await page.goto('https://iflow.cn/?open=setting', { 
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });
    
    await sleep(3000);
    await page.screenshot({ path: join(SCREENSHOT_DIR, 'iflow-login.png') });
    
    // 检测是否需要登录
    let needsLogin = await page.evaluate(() => {
      const allText = document.body.innerText.toLowerCase();
      return allText.includes('登录') || allText.includes('login');
    });
    
    if (needsLogin) {
      log('⚠️  检测到需要登录...', 'yellow');
      console.log('');
      console.log('   请在打开的浏览器窗口中完成登录...');
      console.log('');
      
      for (let i = 0; i < 12; i++) {
        await sleep(10000);
        log(`⏳ 等待登录... (${(i + 1) * 10}秒)`, 'blue');
        
        needsLogin = await page.evaluate(() => {
          const allText = document.body.innerText.toLowerCase();
          return allText.includes('登录') || allText.includes('login');
        });
        
        if (!needsLogin) {
          log('✅ 检测到登录成功！', 'green');
          break;
        }
      }
    }
    
    await sleep(3000);
    await page.screenshot({ path: join(SCREENSHOT_DIR, 'iflow-logged-in.png') });
    
    // 查找 API Key
    log('🔍 查找 API Key...', 'blue');
    
    // 方法 1: 查找输入框
    let apiKey = await page.evaluate(() => {
      const inputs = document.querySelectorAll('input');
      for (const input of inputs) {
        const value = input.value || '';
        if (value.startsWith('sk-') && value.length > 35) {
          return value.trim();
        }
        const placeholder = input.placeholder || '';
        if (placeholder.toLowerCase().includes('api') || placeholder.includes('密钥')) {
          // 找到相关输入框，尝试读取
          return input.value || '';
        }
      }
      return null;
    });
    
    // 方法 2: 查找包含 sk-的文本
    if (!apiKey) {
      apiKey = await page.evaluate(() => {
        const allText = document.body.innerText;
        const matches = allText.match(/sk-[a-zA-Z0-9]{32}/g);
        if (matches && matches.length > 0) {
          return matches[0];
        }
        return null;
      });
    }
    
    // 方法 3: 查找"复制"按钮并点击
    if (!apiKey) {
      log('🔘 尝试查找复制按钮...', 'blue');
      
      const copyButton = await page.evaluate(() => {
        const buttons = document.querySelectorAll('button, [role="button"], span, div');
        for (const btn of buttons) {
          const text = btn.textContent.toLowerCase();
          if (text.includes('复制') || text.includes('copy')) {
            // 返回按钮的选择器
            return btn.id || btn.className?.split(' ')[0] || null;
          }
        }
        return null;
      });
      
      if (copyButton) {
        log('📋 找到复制按钮，尝试点击...', 'blue');
        // 点击复制按钮
        try {
          await page.click(`#${copyButton}`);
        } catch {
          try {
            await page.click(`.${copyButton}`);
          } catch {
            log('⚠️  无法点击复制按钮', 'yellow');
          }
        }
        
        await sleep(1000);
        
        // 从剪贴板读取
        try {
          const { stdout } = await execAsync('pbpaste');
          const clipboardContent = stdout.trim();
          if (clipboardContent.startsWith('sk-') && clipboardContent.length > 35) {
            apiKey = clipboardContent;
            log('✅ 从剪贴板获取到 API Key!', 'green');
          }
        } catch (e) {
          log('⚠️  无法读取剪贴板', 'yellow');
        }
      }
    }
    
    // 方法 4: 截图让用户手动查看
    await page.screenshot({ path: join(SCREENSHOT_DIR, 'iflow-final.png') });
    
    if (apiKey && apiKey.startsWith('sk-')) {
      log('✅ 成功获取 API Key!', 'green');
      console.log('');
      console.log(`   Key: ${apiKey}`);
      console.log('');
      
      // 自动更新配置
      log('🔄 自动更新配置...', 'blue');
      
      try {
        await execAsync(`~/.openclaw/workspace/scripts/iflow-update-key.sh ${apiKey}`);
        log('✅ 配置更新完成!', 'green');
      } catch (e) {
        log(`⚠️  自动更新失败：${e.message}`, 'yellow');
        console.log('');
        console.log('   请手动运行：');
        console.log(`   ~/.openclaw/workspace/scripts/iflow-update-key.sh ${apiKey}`);
      }
      
      await browser.close();
      return apiKey;
    } else {
      log('⚠️  未能自动获取 API Key', 'yellow');
      console.log('');
      console.log('   截图已保存到：' + join(SCREENSHOT_DIR, 'iflow-final.png'));
      console.log('');
      console.log('   请手动复制 API Key，然后告诉我：');
      console.log('   "更新 iFlow Key: sk-xxxxx"');
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

getIfloApiKey()
  .then(key => {
    if (key) {
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
