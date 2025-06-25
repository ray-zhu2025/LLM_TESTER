#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能模型测试脚本 - 简洁版本
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Any
from evalscope.perf.main import run_perf_benchmark
from evalscope.perf.arguments import Arguments


def get_models(base_url: str) -> List[str]:
    """获取可用模型列表"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=10)
        if response.status_code == 200:
            models_data = response.json()
            models = []
            for model in models_data.get('models', []):
                model_name = model.get('name', '')
                # 过滤掉embedding模型
                if model_name and 'embedding' not in model_name.lower():
                    models.append(model_name)
            return models
    except Exception as e:
        print(f"获取模型列表失败: {e}")
    return ["qwen3:32b"]


def test_model(model: str, base_url: str, config_type: str) -> Dict[str, Any]:
    """测试单个模型"""
    print(f"测试模型: {model}")
    
    # 根据配置类型设置参数
    if config_type == "quick":
        parallel = [1, 5, 10]
        number = [5, 10, 15]
        tokens = 512
        prompt_length = 100
    elif config_type == "stress":
        parallel = [50]
        number = [200]
        tokens = 2048
        prompt_length = 500
    else:  # full
        parallel = [1, 5, 10, 15, 25, 40, 65]
        number = [10, 10, 20, 30, 50, 80, 130]
        tokens = 1024
        prompt_length = 200
    
    try:
        config = Arguments(
            parallel=parallel,
            number=number,
            model=model,
            url=f"{base_url}/v1/chat/completions",
            api='openai',
            dataset='openqa',
            min_tokens=tokens,
            max_tokens=tokens,
            prefix_length=0,
            min_prompt_length=50,
            max_prompt_length=prompt_length,
            extra_args={'ignore_eos': True},
            swanlab_api_key='U4ZjjjOSZek5bchapgBtR',
            name=f'{model}-{config_type}-test'
        )
        
        start_time = time.time()
        results = run_perf_benchmark(config)
        test_time = time.time() - start_time
        
        return {
            'model': model,
            'status': 'success',
            'test_time': test_time,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'model': model,
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="模型性能测试")
    parser.add_argument("--config", choices=["quick", "full", "stress"], 
                       default="full", help="测试配置")
    parser.add_argument("--models", nargs="+", help="指定模型")
    parser.add_argument("--url", default="http://10.103.80.5:11434", 
                       help="API地址")
    
    args = parser.parse_args()
    
    print(f"开始测试 (配置: {args.config})")
    
    # 获取模型列表
    if args.models:
        models = args.models
    else:
        models = get_models(args.url)
    
    print(f"测试模型: {', '.join(models)}")
    
    # 测试所有模型
    results = []
    for i, model in enumerate(models, 1):
        print(f"\n进度: {i}/{len(models)}")
        result = test_model(model, args.url, args.config)
        results.append(result)
        
        if result['status'] == 'success':
            print(f"✅ {model}: 成功 ({result['test_time']:.2f}秒)")
        else:
            print(f"❌ {model}: {result['error']}")
        
        if i < len(models):
            time.sleep(3)
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_{args.config}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存: {filename}")
    
    # 统计
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"成功: {success_count}/{len(models)}")


if __name__ == "__main__":
    main() 