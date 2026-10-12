import time
from multiprocessing import Pool

def _process_chunk(chunk):
    """Helper function to process a chunk of the dataset in a worker process."""
    total = sum(chunk)
    minimum = min(chunk) if chunk else 0
    maximum = max(chunk) if chunk else 0
    even_count = sum(1 for x in chunk if x % 2 == 0)
    odd_count = len(chunk) - even_count
    return total, minimum, maximum, even_count, odd_count, len(chunk)

def run_parallel(dataset, num_processes=4):
    """Processes the dataset in parallel using multiprocessing."""
    start_time = time.time()
    
    chunk_size = max(1, len(dataset) // num_processes)
    chunks = [dataset[i:i + chunk_size] for i in range(0, len(dataset), chunk_size)]
    
    actual_processes = min(num_processes, len(chunks))
    
    with Pool(processes=actual_processes) as pool:
        results = pool.map(_process_chunk, chunks)
        
    total_sum = sum(res[0] for res in results)
    min_val = min(res[1] for res in results)
    max_val = max(res[2] for res in results)
    even_count = sum(res[3] for res in results)
    odd_count = sum(res[4] for res in results)
    total_elements = sum(res[5] for res in results)
    
    average = total_sum / total_elements if total_elements > 0 else 0
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return {
        'num_processes': actual_processes,
        'total': total_sum,
        'average': average,
        'minimum': min_val,
        'maximum': max_val,
        'even_count': even_count,
        'odd_count': odd_count,
        'execution_time': execution_time
    }
