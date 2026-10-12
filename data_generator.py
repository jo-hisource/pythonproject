import random
import os
import csv

def generate_dataset(size):
    """Generates a list of random integers."""
    return [random.randint(1, 100000) for _ in range(size)]

def save_results_to_csv(bench_results):
    """Saves benchmark results to a CSV file inside the results directory."""
    os.makedirs("results", exist_ok=True)
    file_path = os.path.join("results", "performance_results.csv")
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Dataset Size", "Sequential Time (s)", "Parallel Time (s)", "Speedup"])
        for res in bench_results:
            writer.writerow([res['size'], res['seq_time'], res['par_time'], res['speedup']])