# iFlow 研究报告

## 1. iFlow 是什么产品/服务？

**iFlow（心流）** 是阿里巴巴心流 AI 团队推出的**终端 AI 智能体工具**，堪称**国产版"Claude Code"**。

### 核心定位
- **产品名称**：iFlow CLI（心流开放平台）
- **产品类型**：终端 AI 助手/智能体
- **开发团队**：阿里巴巴心流 AI 团队
- **发布时间**：2025 年 7 月（GitHub 仓库创建时间）
- **GitHub 仓库**：https://github.com/iflow-ai/iflow-cli
- **Star 数**：5000+（截至 2026 年 3 月）

### 核心特性
1. **终端集成**：直接在终端中运行的 AI 助手
2. **代码分析**：无缝分析代码仓库、执行编程任务
3. **自然语言交互**：用日常对话驱动 AI，无需记忆复杂命令
4. **多模型支持**：支持 Qwen3 MAX、Kimi K2、DeepSeek V3.2、GLM4.6 等顶级模型
5. **开放平台**：可一键安装 SubAgent 和 MCP，快速扩展智能体能力

---

## 2. 官网和文档地址

### 官方网站
- **心流开放平台**：https://platform.iflow.cn
- **iFlow CLI 官网**：https://cli.iflow.cn
- **备用官网**：https://iflow.cn

### 文档地址
- **快速开始**：https://platform.iflow.cn/cli/quickstart
- **完整文档**：https://platform.iflow.cn/cli/
- **GitHub README**：https://github.com/iflow-ai/iflow-cli/blob/main/README_CN.md
- **模型库**：https://platform.iflow.cn/models
- **MCP 市场**：https://platform.iflow.cn/（导航栏）

### 社区交流
- **GitHub Issues**：https://github.com/iflow-ai/iflow-cli/issues
- **微信群**：通过 GitHub README 中的二维码加入

---

## 3. 免费 API 和免费套餐

### ✅ 免费政策

**iFlow CLI 面向个人用户永久免费**，具体包括：

| 项目 | 免费政策 |
|------|----------|
| **使用次数** | 不限制 |
| **流量** | 不限制 |
| **模型调用** | 免费调用 Qwen3 MAX、Kimi K2、DeepSeek V3.2、GLM4.6 等顶级模型 |
| **有效期** | 不限期，随时可用 |
| **功能** | 完整功能支持（WebSearch、WebFetch、多模态等） |

### 认证方式

iFlow 提供三种登录/认证方式：

#### 方式一：Login with iFlow（推荐）
- **功能**：完整功能支持
  - ✅ WebSearch 服务（智能网络搜索）
  - ✅ WebFetch 服务（网页内容抓取）
  - ✅ 多模态能力（图像理解等）
  - ✅ 工具调用优化
- **步骤**：
  1. 运行 `iflow` 后选择 Login with iFlow
  2. CLI 自动打开浏览器跳转到心流平台
  3. 完成注册/登录后授权
  4. 自动返回终端开始使用

#### 方式二：心流 API Key 登录
- **功能**：与方式一相同，享受完整功能
- **注意**：API Key 有效期为 7 天，需定期更新
- **步骤**：
  1. 访问 https://iflow.cn/?open=setting 完成注册
  2. 在用户设置页面生成 API KEY
  3. 在 iFlow CLI 中选择 API Key 登录并输入密钥

#### 方式三：OpenAI Compatible API
- **功能**：有限制
  - ❌ 不支持 WebSearch 服务
  - ❌ 不支持 WebFetch 服务
  - ❌ 不支持心流平台的内置多模态能力
  - ❌ 无法享受心流平台模型的工具调用优化
- **适用场景**：使用自有模型服务或其他兼容 OpenAI 协议的服务

### API 端点
- **Base URL**：`https://apis.iflow.cn/v1`
- **认证**：通过 iFlow 平台 API Key

---

## 4. iFlow 与 OpenClaw 集成方案

### 集成方式分析

iFlow 与 OpenClaw 都是终端 AI 助手工具，但定位有所不同：

| 特性 | iFlow CLI | OpenClaw |
|------|-----------|----------|
| **定位** | 终端 AI 智能体/编程助手 | AI 代理框架/技能平台 |
| **核心功能** | 代码分析、文件操作、任务执行 | 技能管理、子代理、工具调用 |
| **扩展方式** | SubAgent、MCP、自定义 Command | Skills、Subagents、Tools |
| **模型支持** | 心流平台免费模型 + OpenAI 兼容 | 多模型支持（通过配置） |
| **开源程度** | 部分开源（CLI 工具） | 开源框架 |

### 可能的集成方案

#### 方案一：将 iFlow 作为 OpenClaw 的底层 AI 引擎
利用 iFlow 的免费模型 API，替换 OpenClaw 的模型调用层。

**配置步骤**：
1. 在 OpenClaw 配置文件中添加 iFlow API 端点
2. 配置 iFlow API Key（通过心流平台获取）
3. 修改模型调用逻辑，使用 OpenAI 兼容接口

**配置文件示例**（`~/.openclaw/config.json` 或类似）：
```json
{
  "models": {
    "iflow": {
      "baseUrl": "https://apis.iflow.cn/v1",
      "apiKey": "YOUR_IFLOW_API_KEY",
      "modelName": "Qwen3-Coder"
    }
  }
}
```

#### 方案二：将 iFlow 作为 OpenClaw 的技能/工具
将 iFlow CLI 封装为 OpenClaw 的一个技能，通过 exec 调用。

**技能实现**：
```bash
# 创建技能目录
mkdir -p ~/.openclaw/workspace/skills/iflow-cli

# 创建 SKILL.md
cat > ~/.openclaw/workspace/skills/iflow-cli/SKILL.md << 'EOF'
# iFlow CLI 技能

使用 iFlow CLI 执行终端 AI 任务。

## 触发条件
- 用户请求代码分析、文件操作、编程任务
- 用户提到 "用 iflow" 或 "心流"

## 使用方法
1. 确保已安装 iFlow CLI：`npm i -g @iflow-ai/iflow-cli`
2. 确保已认证：运行 `iflow` 完成登录
3. 通过 exec 调用 iFlow 命令

## 示例命令
- `iflow --version` - 查看版本
- `echo "分析这个项目" | iflow` - 执行任务
EOF
```

#### 方案三：使用 iFlow 的 MCP 服务器
iFlow 支持 MCP（Model Context Protocol），可以作为 MCP 服务器为 OpenClaw 提供服务。

**步骤**：
1. 在 iFlow 中配置 MCP 服务器
2. 在 OpenClaw 中配置 MCP 客户端连接
3. 通过 MCP 协议交换消息和工具调用

---

## 5. iFlow 的主要功能和使用场景

### 核心功能

#### 1. 代码分析与开发
- 项目结构分析（`/init` 命令）
- 代码审查和优化建议
- 自动生成代码和文档
- Bug 定位和修复

#### 2. 文件操作
- 文件创建、编辑、删除
- 批量文件处理
- 文件内容分析和整理
- 目录结构优化建议

#### 3. Shell 命令辅助
- 执行系统命令（`!命令`）
- 命令解释和建议
- 自动化脚本生成
- 系统任务自动化

#### 4. 信息查询与规划
- 网络搜索（WebSearch）
- 网页内容抓取（WebFetch）
- 旅行规划、餐厅推荐
- 价格对比和研究

#### 5. 数据分析
- Excel/CSV 文件分析
- 数据可视化和图表生成
- 数据提取和合并
- 销售数据分析

#### 6. 工作流自动化
- 定时任务脚本
- 文件备份自动化
- 邮件通知系统
- 企业协作套件集成

### 运行模式

iFlow 支持 4 种运行模式：

| 模式 | 权限 | 说明 |
|------|------|------|
| **yolo 模式** | 最大权限 | 模型可执行任何操作 |
| **接受编辑模式** | 文件修改权限 | 模型仅可修改文件 |
| **计划模式** | 需确认 | 先计划后执行 |
| **默认模式** | 无权限 | 仅提供建议 |

### 特色功能

1. **SubAgent（子代理）**：将 CLI 从通用助手转变为专家团队
2. **Task 工具**：有效压缩上下文长度，自动压缩（70% 阈值）
3. **多模态能力**：支持图片粘贴和理解（Ctrl+V）
4. **对话历史**：支持保存和回滚（`iflow --resume` 和 `/chat` 命令）
5. **开放市场**：一键安装 MCP 工具、Subagents、自定义指令和工作流
6. **自动更新**：启动时检测并自动更新到最新版本
7. **IDE 插件**：支持 VS Code 和 JetBrains 插件

---

## 6. 接入 OpenClaw 的具体步骤

### 步骤一：安装 iFlow CLI

```bash
# macOS/Linux（推荐一键安装）
bash -c "$(curl -fsSL https://cloud.iflow.cn/iflow-cli/install.sh)"

# 或使用 npm 安装
npm i -g @iflow-ai/iflow-cli@latest

# 验证安装
iflow --version
```

### 步骤二：配置 iFlow 认证

```bash
# 启动 iFlow
iflow

# 选择登录方式：
# 1. Login with iFlow（推荐，浏览器自动登录）
# 2. API Key 登录（服务器环境使用）
```

获取 API Key（如需）：
1. 访问 https://iflow.cn/?open=setting
2. 完成注册/登录
3. 在设置页面生成 API Key（有效期 7 天）

### 步骤三：在 OpenClaw 中集成 iFlow

#### 方案 A：创建 iFlow 技能（推荐）

```bash
# 创建技能目录
mkdir -p ~/.openclaw/workspace/skills/iflow

# 创建 SKILL.md
cat > ~/.openclaw/workspace/skills/iflow/SKILL.md << 'SKILL_EOF'
# iFlow 集成技能

使用 iFlow CLI 执行终端 AI 任务，利用免费的高质量 AI 模型。

## 触发条件
- 用户请求代码分析、文件操作、编程任务
- 用户提到 "用 iflow"、"心流" 或 "免费 AI 模型"
- 需要执行复杂的终端 AI 任务

## 前置条件
1. 已安装 iFlow CLI：`npm i -g @iflow-ai/iflow-cli`
2. 已完成认证：运行 `iflow` 完成登录

## 使用方法

### 直接调用
```bash
# 执行简单任务
echo "分析这个项目的结构" | iflow

# 交互式任务
iflow << 'EOF'
分析 @src 目录下的代码结构
生成技术文档
EOF
```

### 通过 exec 工具
使用 OpenClaw 的 exec 工具调用 iFlow 命令。

## 注意事项
- API Key 有效期 7 天，需定期更新
- 建议使用 Login with iFlow 方式，避免手动更新
- 确保网络连接正常（需要访问 apis.iflow.cn）
SKILL_EOF
```

#### 方案 B：配置 iFlow 为 OpenClaw 的模型后端

如果 OpenClaw 支持自定义模型端点：

1. 编辑 OpenClaw 配置文件（如 `~/.openclaw/config.json`）
2. 添加 iFlow 模型配置：

```json
{
  "models": {
    "iflow-qwen3": {
      "provider": "openai-compatible",
      "baseUrl": "https://apis.iflow.cn/v1",
      "apiKey": "YOUR_IFLOW_API_KEY",
      "modelName": "Qwen3-Coder"
    },
    "iflow-kimi": {
      "provider": "openai-compatible",
      "baseUrl": "https://apis.iflow.cn/v1",
      "apiKey": "YOUR_IFLOW_API_KEY",
      "modelName": "Kimi-K2"
    }
  }
}
```

3. 重启 OpenClaw 使配置生效

### 步骤四：测试集成

```bash
# 测试 iFlow CLI 是否正常工作
cd ~/.openclaw/workspace
iflow << 'EOF'
分析这个项目的结构和主要功能
EOF

# 测试 OpenClaw 是否能调用 iFlow 技能
# （根据 OpenClaw 的具体调用方式）
```

### 步骤五：使用场景示例

#### 场景 1：代码项目分析
```bash
# 在 OpenClaw 中调用 iFlow 技能
cd your-project/
iflow
> /init
> 分析这个项目的结构和主要功能
```

#### 场景 2：文件批量处理
```bash
iflow
> 将我桌面上的文件按文件类型整理到不同的文件夹中
```

#### 场景 3：数据分析
```bash
iflow
> 分析这个 Excel 表格中的销售数据，生成简单的图表
```

#### 场景 4：工作流自动化
```bash
iflow
> 创建一个脚本，定期将我的重要文件备份到云存储
```

---

## 7. 总结与建议

### iFlow 的优势
1. **完全免费**：个人用户永久免费，不限流量和次数
2. **高质量模型**：支持 Qwen3 MAX、Kimi K2 等顶级模型
3. **本土化优化**：中文处理和本土化体验优势明显
4. **功能完整**：WebSearch、WebFetch、多模态等完整支持
5. **易于集成**：OpenAI 兼容 API，支持 MCP 协议

### 与 OpenClaw 集成的价值
1. **降低成本**：使用 iFlow 的免费模型替代付费模型
2. **增强能力**：利用 iFlow 的终端 AI 能力扩展 OpenClaw
3. **互补优势**：OpenClaw 的技能管理 + iFlow 的终端执行

### 推荐集成方案
**首选方案**：将 iFlow 作为 OpenClaw 的底层模型后端（方案 A）
- 配置简单，只需修改模型端点
- 充分利用 iFlow 的免费模型资源
- 保持 OpenClaw 的技能和子代理架构

**备选方案**：将 iFlow 封装为 OpenClaw 的技能（方案 B）
- 适用于需要独立调用 iFlow 的场景
- 可以作为特殊任务的专用工具

### 注意事项
1. API Key 有效期 7 天，需定期更新（建议使用 Login with iFlow 方式）
2. 需要稳定的网络连接访问 apis.iflow.cn
3. 关注 iFlow 平台的政策变化（目前免费，未来可能调整）

---

## 参考资料

- iFlow GitHub：https://github.com/iflow-ai/iflow-cli
- 心流开放平台：https://platform.iflow.cn
- 快速开始文档：https://platform.iflow.cn/cli/quickstart
- AI 工具集介绍：https://ai-bot.cn/sites/64688.html
- 知乎专栏：https://zhuanlan.zhihu.com/p/1945981267138027570

---

*研究报告生成时间：2026 年 3 月 11 日*
*信息来源：官方文档、GitHub 仓库、第三方评测*
