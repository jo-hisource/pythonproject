import time

def run_sequential(dataset):
    """Processes the dataset sequentially and measures execution time."""
    start_time = time.time()
    
    total = sum(dataset)
    count = len(dataset)
    average = total / count if count > 0 else 0
    minimum = min(dataset) if count > 0 else 0
    maximum = max(dataset) if count > 0 else 0
    
    even_count = sum(1 for x in dataset if x % 2 == 0)
    odd_count = count - even_count
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return {
        'total': total,
        'average': average,
        'minimum': minimum,
        'maximum': maximum,
        'even_count': even_count,
        'odd_count': odd_count,
        'execution_time': execution_time
    }