#!/usr/bin/env node
/**
 * iFlow API Key 自动获取脚本 v3
 * 改进版：点击"复制密钥"按钮，从剪贴板读取
 */

import { chromium } from 'playwright';
import { writeFile } from 'fs/promises';
import { join } from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const SCREENSHOT_DIR = '/Users/jesson/.openclaw/workspace/screenshots';
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
  log('🚀 启动 iFlow API Key 自动获取 v3 (点击复制)...', 'cyan');
  console.log('');
  
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--window-size=1280,800', '--disable-blink-features=AutomationControlled'],
    ignoreDefaultArgs: ['--enable-automation']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    bypassCSP: true,
    permissions: ['clipboard-read', 'clipboard-write']
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
    
    // 查找"API 管理"或"API Key"相关按钮并点击
    log('🔍 查找 API 管理弹窗...', 'blue');
    
    // 尝试点击 API Key 相关按钮
    const apiButtonClicked = await page.evaluate(() => {
      // 查找包含"API"的按钮
      const buttons = document.querySelectorAll('button, [role="button"], span, div');
      for (const btn of buttons) {
        const text = btn.textContent;
        if (text.includes('API') || text.includes('密钥') || text.includes('Key')) {
          btn.click();
          return true;
        }
      }
      return false;
    });
    
    await sleep(2000);
    
    // 查找"复制密钥"按钮并点击
    log('📋 查找"复制密钥"按钮...', 'blue');
    
    const copyButtonFound = await page.evaluate(() => {
      const buttons = document.querySelectorAll('button, [role="button"]');
      for (const btn of buttons) {
        const text = btn.textContent;
        if (text.includes('复制') || text.includes('Copy')) {
          btn.click();
          return true;
        }
      }
      return false;
    });
    
    if (copyButtonFound) {
      log('✅ 已点击复制按钮', 'green');
      await sleep(1000);
      
      // 从剪贴板读取
      try {
        const { stdout } = await execAsync('pbpaste');
        const clipboardContent = stdout.trim();
        
        if (clipboardContent.startsWith('sk-') && clipboardContent.length > 35) {
          log('✅ 从剪贴板获取到 API Key!', 'green');
          console.log('');
          console.log(`   Key: ${clipboardContent}`);
          console.log('');
          
          // 自动更新配置
          log('🔄 自动更新配置...', 'blue');
          console.log('');
          
          // 保存到临时文件
          await writeFile('/tmp/iflow-new-key.txt', clipboardContent);
          
          console.log('   请运行以下命令更新配置：');
          console.log('');
          console.log(`   ~/.openclaw/workspace/scripts/iflow-update-key.sh ${clipboardContent}`);
          console.log('');
          
          await browser.close();
          return clipboardContent;
        } else {
          log('⚠️  剪贴板内容不是有效的 API Key', 'yellow');
          console.log(`   剪贴板内容：${clipboardContent.substring(0, 50)}...`);
        }
      } catch (e) {
        log(`⚠️  无法读取剪贴板：${e.message}`, 'yellow');
      }
    }
    
    // 截图保存
    await page.screenshot({ path: join(SCREENSHOT_DIR, 'iflow-final.png') });
    
    log('⚠️  未能自动获取 API Key', 'yellow');
    console.log('');
    console.log('   截图已保存到：' + join(SCREENSHOT_DIR, 'iflow-final.png'));
    console.log('');
    console.log('   请手动点击"复制密钥"按钮，然后告诉我：');
    console.log('   "更新 iFlow Key: sk-xxxxx"');
    console.log('');
    
    await browser.close();
    return null;
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
