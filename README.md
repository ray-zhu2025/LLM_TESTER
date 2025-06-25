# EvalScope - 大语言模型性能评估工具包

EvalScope 是一个用于评估大语言模型性能的工具包。目前主要支持对 Qwen 系列模型进行性能测试，支持多种接口类型。

## 🚀 功能特点

- 支持多并发测试（1-200并发）
- 自动获取可用模型列表
- 详细的性能指标统计
- 支持自定义测试参数
- 支持 OpenAI 兼容接口和 Ollama 接口
- 多种测试配置（快速、完整、压力测试）

## 📁 脚本文件

- **`vllm_benchmark.py`** - vLLM接口测试脚本
- **`ollama_benchmark.py`** - Ollama接口测试脚本
- **`run.sh`** - 自动化测试脚本
- **`run_benchmark.py`** - 原始单模型测试脚本

## 🔧 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/evalscope.git
cd evalscope
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 📖 使用方法

### vLLM接口测试
```bash
# 完整测试（默认）
python vllm_benchmark.py

# 快速测试
python vllm_benchmark.py --config quick

# 压力测试
python vllm_benchmark.py --config stress

# 测试指定模型
python vllm_benchmark.py --models Qwen3-32B

# 指定API地址
python vllm_benchmark.py --url http://your-vllm-server:8001
```

### Ollama接口测试
```bash
# 完整测试（默认）
python ollama_benchmark.py

# 快速测试
python ollama_benchmark.py --config quick

# 压力测试
python ollama_benchmark.py --config stress

# 测试指定Ollama模型
python ollama_benchmark.py --models llama3.2 qwen2.5

# 指定Ollama地址
python ollama_benchmark.py --url http://your-ollama-server:11434
```

### 自动化测试
```bash
# 给脚本添加执行权限
chmod +x run.sh

# 运行自动化测试（先vLLM，后Ollama）
./run.sh
```

## ⚙️ 配置说明

### 测试配置类型

1. **quick** - 快速测试
   - 并发数: [1, 5, 10]
   - 请求数: [5, 10, 15]
   - Token数: 512
   - 提示长度: 100

2. **full** - 完整测试（默认）
   - 并发数: [1, 5, 10, 15, 25, 40, 65]
   - 请求数: [10, 10, 20, 30, 50, 80, 130]
   - Token数: 1024
   - 提示长度: 200

3. **stress** - 压力测试
   - 并发数: [1, 10, 25, 50]
   - 请求数: [20, 50, 100, 200]
   - Token数: 2048
   - 提示长度: 500

## 📊 性能指标

测试结果包含以下指标：
- 平均延迟 (avg_latency)
- 最小延迟 (min_latency)
- 最大延迟 (max_latency)
- P50延迟 (p50_latency)
- P90延迟 (p90_latency)
- P99延迟 (p99_latency)
- 成功率 (success_rate)
- 每秒请求数 (requests_per_second)
- 输出token吞吐量 (output_token_throughput)
- 总token吞吐量 (total_token_throughput)
- 首token时间 (time_to_first_token)
- 每token时间 (time_per_output_token)

## 📁 输出结果

- **控制台**: 实时进度和状态
- **JSON文件**: 
  - vLLM: `benchmark_{config}_{timestamp}.json`
  - Ollama: `ollama_benchmark_{config}_{timestamp}.json`
- **包含**: 模型信息、测试结果、时间戳、错误信息
- **SwanLab**: 自动同步到云端进行实验跟踪

## 🔧 接口特定说明

### vLLM接口
- 默认端口: 8001
- 使用 `/v1/models` 获取可用模型列表
- 支持 `/v1/chat/completions` 接口

### Ollama接口
- 默认端口: 11434
- 使用 `/api/tags` 获取可用模型列表
- 支持OpenAI兼容的 `/v1/chat/completions` 接口
- 自动过滤embedding模型

## ⚠️ 注意事项

1. 确保API服务正在运行
2. 检查网络连接
3. 高并发测试需要足够系统资源
4. 测试结果自动保存为JSON文件
5. 建议先从低并发开始测试
6. 注意观察API服务的负载情况

## 🐛 故障排除

- **连接超时**: 检查API服务状态和URL
- **模型不存在**: 确认模型名称正确
- **测试失败**: 查看错误信息和API日志
- **SwanLab错误**: 检查API密钥和网络连接

## 🔄 自定义测试

你可以通过修改脚本中的参数来自定义测试：
- 并发数列表
- 请求数量
- 输入输出token长度
- API端口
- 其他参数

## 📈 示例结果

测试完成后会生成详细的性能报告，包括：
- 基础信息（模型、总生成量、测试时间、平均输出速率）
- 详细性能指标表格
- 最佳性能配置推荐
- 性能优化建议 