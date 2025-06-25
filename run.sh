#!/bin/bash

# Activate uv environment
echo "🐍 Activating uv virtual environment..."
source .venv/bin/activate

# 模型性能测试运行脚本
# 使用 stress 模式，固定模型为 qwen3:32b

echo "🚀 开始模型性能测试 (Stress 模式)"
echo "📋 测试模型: qwen3:32b"
echo ""

# 创建结果目录
mkdir -p results
timestamp=$(date +"%Y%m%d_%H%M%S")

echo "=" * 50
echo "📊 测试 1: vLLM 接口测试"
echo "=" * 50

# 运行 vLLM 测试
echo "🔍 开始 vLLM 测试..."
python vllm_benchmark.py --config stress --models Qwen3-32B

if [ $? -eq 0 ]; then
    echo "✅ vLLM 测试完成"
else
    echo "❌ vLLM 测试失败"
fi

echo ""
echo "⏳ 等待 10 秒后开始下一个测试..."
sleep 10

echo "=" * 50
echo "📊 测试 2: Ollama 接口测试"
echo "=" * 50

# 运行 Ollama 测试
echo "🔍 开始 Ollama 测试..."
python ollama_benchmark.py --config stress --models qwen3:32b

if [ $? -eq 0 ]; then
    echo "✅ Ollama 测试完成"
else
    echo "❌ Ollama 测试失败"
fi

echo ""
echo "🎉 所有测试完成！"
echo "📁 结果文件已保存到当前目录"
echo "📊 请查看生成的 JSON 文件获取详细结果" 