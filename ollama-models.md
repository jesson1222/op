# Ollama Models - Backup Configuration

Generated: 2026-02-26

## Local Models

| Model | Size | Modified |
|-------|------|----------|
| qwen3.5:35b | 23 GB | 10 hours ago |
| llama3.1:8b | 4.9 GB | 15 hours ago |
| qwen3:30b | 18 GB | 2 weeks ago |
| gemma3:4b | 3.3 GB | 2 weeks ago |
| gemma3:1b | 815 MB | 2 weeks ago |
| qwen3:4b | 2.5 GB | 2 weeks ago |

## Cloud Models

| Model | Modified |
|-------|----------|
| qwen3-vl:235b-cloud | 12 hours ago |
| glm-4.6:cloud | 2 days ago |
| gpt-oss:20b-cloud | 3 months ago |
| qwen3-coder:480b-cloud | 3 months ago |
| gpt-oss:120b-cloud | 3 months ago |
| deepseek-v3.1:671b-cloud | 3 months ago |

## Fallback Priority (Recommended)

1. **Primary:** `qwen3.5:35b` - Best balance of performance & capability
2. **Fast/Local:** `llama3.1:8b` - Quick responses, smaller footprint
3. **Lightweight:** `gemma3:1b` - Minimal resource usage
4. **Cloud Fallback:** `glm-4.6:cloud` - When local models insufficient
5. **Heavy Duty:** `qwen3-coder:480b-cloud` - Complex coding tasks
6. **Vision:** `qwen3-vl:235b-cloud` - Image understanding

## Usage Notes

- Local models: No API key needed, run offline
- Cloud models: Require internet connection
- Total local storage: ~48 GB
