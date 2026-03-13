#!/bin/bash
# iFlow CLI 包装脚本
# 使用 OAuth 认证（自动续期）

export IFLOW_BASE_URL="https://apis.iflow.cn/v1"
export IFLOW_MODEL_NAME="qwen3-max"

# OAuth 认证由 iFlow CLI 自动管理，无需 API Key

exec iflow "$@"
