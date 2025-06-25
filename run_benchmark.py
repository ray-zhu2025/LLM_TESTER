from evalscope.perf.main import run_perf_benchmark
from evalscope.perf.arguments import Arguments

def main():
    task_cfg = Arguments(
        parallel=[1, 5, 10, 15, 25, 40, 65],
        number=[10, 10, 20, 30, 50, 80, 130],
        model='Qwen3-32B',
        url='http://10.103.80.5:8001/v1/chat/completions',
        api='openai',
        dataset='openqa',
        min_tokens=1024,
        max_tokens=1024,
        prefix_length=0,
        min_prompt_length=50,
        max_prompt_length=200,
        extra_args={'ignore_eos': True},
        swanlab_api_key='U4ZjjjOSZek5bchapgBtR',
        name='Qwen3-32B-Benchmark-v1'
    )
    
    print("开始性能测试...")
    results = run_perf_benchmark(task_cfg)
    print("测试完成！")
    print("结果：", results)

if __name__ == "__main__":
    main() 