from data_generator import generate_dataset
from sequential import run_sequential
from parallel import run_parallel

def benchmark_datasets(sizes):
    """Runs performance comparisons across user-provided dataset sizes."""
    benchmark_results = []
    
    for size in sizes:
        dataset = generate_dataset(size)
        
        # Run sequential
        seq_res = run_sequential(dataset)
        seq_time = seq_res['execution_time']
        
        # Run parallel
        par_res = run_parallel(dataset, num_processes=4)
        par_time = par_res['execution_time']
        
        # Calculate speedup
        speedup = seq_time / par_time if par_time > 0 else 0
        
        benchmark_results.append({
            'size': size,
            'seq_time': seq_time,
            'par_time': par_time,
            'speedup': speedup
        })
        
    return benchmark_results