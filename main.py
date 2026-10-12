import os
import sys
import time
from data_generator import generate_dataset, save_results_to_csv
from sequential import run_sequential
from parallel import run_parallel
from performance import benchmark_datasets

# ANSI Color Codes & Styles
GREEN = "\033[92m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

BOX_WIDTH = 52

#  results for Option 5
global_benchmark_history = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewrite(text, delay=0.015):
    """Simulates typewriter effect for text output in green."""
    for char in text:
        sys.stdout.write(GREEN + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)

def print_box_header(title):
    print(f"{WHITE}┌" + "─" * (BOX_WIDTH - 2) + "┐")
    title_padded = title.center(BOX_WIDTH - 2)
    print(f"│{BOLD}{title_padded}{RESET}{WHITE}│")
    print(f"├" + "─" * (BOX_WIDTH - 2) + "┤")

def print_box_row(label, val_str, extra_label=""):
    extra_part = f" {extra_label}" if extra_label else ""
    visible_content = f"  {label:<13}: {val_str}{extra_part}"
    padding = (BOX_WIDTH - 2) - len(visible_content)
    if padding < 0:
        padding = 0
    print(f"│{WHITE}  {label:<13}: {GREEN}{val_str}{WHITE}{extra_part}{' ' * padding}│")

def print_menu_row(l_num, l_text, r_num, r_text):
    left_vis = f"  {l_num}: {l_text:<17}"
    right_vis = f"{r_num}: {r_text:<15}"
    total_vis_len = len(left_vis) + len(right_vis)
    padding = (BOX_WIDTH - 2) - total_vis_len
    if padding < 0:
        padding = 0
    
    left_colored = f"  {GREEN}{l_num}{WHITE}: {l_text:<17}"
    right_colored = f"{GREEN}{r_num}{WHITE}: {r_text:<15}"
    print(f"│{left_colored}{right_colored}{' ' * padding}│")

def print_box_footer():
    print(f"└" + "─" * (BOX_WIDTH - 2) + f"┘{RESET}")

def print_intro():
    clear_screen()
    print_box_header("PARALLEL TASK PROCESSING")
    print(f"│{' ' * (BOX_WIDTH - 2)}│")
    
    msg = "Welcome! Would you like to begin?"
    inner_content = f"  {msg}"
    padding_msg = (BOX_WIDTH - 2) - len(inner_content)
    if padding_msg < 0:
        padding_msg = 0
        
    sys.stdout.write("│")
    typewrite(inner_content, delay=0.015)
    print(f"{' ' * padding_msg}│")
    
    print(f"│{' ' * (BOX_WIDTH - 2)}│")
    
    action_vis = "  [S] START    │    [E] EXIT"
    padding_action = (BOX_WIDTH - 2) - len(action_vis)
    if padding_action < 0:
        padding_action = 0
    print(f"│  {BOLD}[S]{RESET}{WHITE} START    │    {BOLD}[E]{RESET}{WHITE} EXIT{' ' * padding_action}│")
    print_box_footer()
    
    choice = input(f"\n{WHITE}Enter your choice ({GREEN}s/e{WHITE}): {RESET}").strip().lower()
    if choice != 's':
        sys.exit()

def display_menu():
    print_box_header("MAIN SYSTEM MENU")
    print_menu_row("1", "Generate Data", "4", "Performance Comp")
    print_menu_row("2", "Sequential", "5", "Results Table")
    print_menu_row("3", "Parallel", "6", "Exit")
    print_box_footer()

def exit_program():
    clear_screen()
    print_box_header("SYSTEM EXIT")
    print(f"│{' ' * (BOX_WIDTH - 2)}│")
    
    msg1 = '"Divide the Work. Process in Parallel. Measure."'
    pad1 = (BOX_WIDTH - 2) - len(f"  {msg1}")
    sys.stdout.write("│  ")
    typewrite(msg1, delay=0.015)
    print(f"{' ' * pad1}│")
    
    msg2 = "Goodbye!"
    pad2 = (BOX_WIDTH - 2) - len(f"  {msg2}")
    sys.stdout.write("│  ")
    typewrite(msg2, delay=0.015)
    print(f"{' ' * pad2}│")
    
    print(f"│{' ' * (BOX_WIDTH - 2)}│")
    
    action_vis = "  [R] Restart Program  │  [E] Exit"
    pad_action = (BOX_WIDTH - 2) - len(action_vis)
    if pad_action < 0:
        pad_action = 0
    print(f"│  {BOLD}[R]{RESET}{WHITE} Restart Program  │  {BOLD}[E]{RESET}{WHITE} Exit{' ' * pad_action}│")
    print_box_footer()
    
    choice = input(f"\n{WHITE}Select action ({GREEN}r/e{WHITE}): {RESET}").strip().lower()
    if choice == 'r':
        main()
    else:
        sys.exit()

def main():
    print_intro()
    
    current_dataset = None
    seq_results = None
    par_results = None
    
    while True:
        clear_screen()
        display_menu()
        choice = input(f"{WHITE}Enter your choice ({GREEN}1-6{WHITE}): {RESET}").strip()
        
        clear_screen()
        
        if choice == '1':
            print_box_header("DATASET CONFIGURATION")
            if current_dataset is None:
                print_box_row("Current Status", "No data generated yet")
            else:
                print_box_row("Current Size", f"{len(current_dataset):,}")
            print_box_footer()
            
            try:
                user_input = input(f"\n{WHITE}Enter dataset size to generate (e.g., 100000): {RESET}").strip()
                dataset_size = int(user_input)
                
                if dataset_size > 0:
                    print(f"\n{WHITE}Generating {dataset_size:,} numbers...{RESET}")
                    current_dataset = generate_dataset(dataset_size)
                    print(f"{GREEN}Data successfully generated! (Size: {dataset_size:,}){RESET}")
                    
                    # Automatically run and save results for the summary table
                    print(f"{WHITE}Running automatic benchmarks for this size...{RESET}")
                    res = benchmark_datasets([dataset_size])
                    global_benchmark_history.extend(res)
                    save_results_to_csv(global_benchmark_history)
                else:
                    print(f"{GREEN}Size must be greater than 0.{RESET}")
            except ValueError:
                print(f"{GREEN}Invalid input! Please enter a valid integer.{RESET}")
                
            seq_results = None
            par_results = None
            
            input(f"\n{WHITE}Press Enter to return to menu...{RESET}")
            
        elif choice == '2':
            if current_dataset is None:
                print_box_header("SEQUENTIAL PROCESSING")
                print_box_row("Error", "No dataset found! Generate data first (Opt 1)")
                print_box_footer()
            else:
                seq_results = run_sequential(current_dataset)
                print_box_header("SEQUENTIAL PROCESSING")
                print_box_row("Dataset Size", f"{len(current_dataset):,}")
                print_box_row("Total Sum", f"{seq_results['total']:,}")
                print_box_row("Average", f"{seq_results['average']:.2f}")
                print_box_row("Minimum", f"{seq_results['minimum']:,}")
                print_box_row("Maximum", f"{seq_results['maximum']:,}")
                print_box_row("Even Numbers", f"{seq_results['even_count']:,}")
                print_box_row("Odd Numbers", f"{seq_results['odd_count']:,}")
                print_box_row("Execution Time", f"{seq_results['execution_time']:.4f}", "sec")
                print_box_footer()
            
            input(f"\n{WHITE}Press Enter to return to menu...{RESET}")
            
        elif choice == '3':
            if current_dataset is None:
                print_box_header("PARALLEL PROCESSING")
                print_box_row("Error", "No dataset found! Generate data first (Opt 1)")
                print_box_footer()
            else:
                par_results = run_parallel(current_dataset, num_processes=4)
                print_box_header("PARALLEL PROCESSING")
                print_box_row("Dataset Size", f"{len(current_dataset):,}")
                print_box_row("Processes", f"{par_results['num_processes']}")
                print_box_row("Total Sum", f"{par_results['total']:,}")
                print_box_row("Average", f"{par_results['average']:.2f}")
                print_box_row("Minimum", f"{par_results['minimum']:,}")
                print_box_row("Maximum", f"{par_results['maximum']:,}")
                print_box_row("Even Numbers", f"{par_results['even_count']:,}")
                print_box_row("Odd Numbers", f"{par_results['odd_count']:,}")
                print_box_row("Execution Time", f"{par_results['execution_time']:.4f}", "sec")
                print_box_footer()
            
            input(f"\n{WHITE}Press Enter to return to menu...{RESET}")
            
        elif choice == '4':
            if current_dataset is None:
                print_box_header("PERFORMANCE COMPARISON")
                print_box_row("Error", "No dataset found! Generate data first (Opt 1)")
                print_box_footer()
            else:
                if not seq_results or not par_results:
                    print(f"{WHITE}Running sequential and parallel processes first...{RESET}")
                    seq_results = run_sequential(current_dataset)
                    par_results = run_parallel(current_dataset, num_processes=4)
                    
                speedup = seq_results['execution_time'] / par_results['execution_time'] if par_results['execution_time'] > 0 else 0
                
                print_box_header("PERFORMANCE COMPARISON")
                print_box_row("Sequential Time", f"{seq_results['execution_time']:.4f}", "sec")
                print_box_row("Parallel Time", f"{par_results['execution_time']:.4f}", "sec")
                print_box_row("Speedup", f"{speedup:.2f}", "x")
                print(f"{WHITE}├" + "─" * (BOX_WIDTH - 2) + "┤")
                status_text = "Parallel was faster for workload." if speedup > 1.0 else "Sequential was faster (overhead)."
                print_box_row("Status", status_text)
                print_box_footer()
                
            input(f"\n{WHITE}Press Enter to return to menu...{RESET}")
            
        elif choice == '5':
            print_box_header("SUMMARY RESULTS TABLE")
            print_box_row("Status", f"{len(global_benchmark_history)} datasets recorded")
            print_box_footer()
            
            if not global_benchmark_history:
                print(f"\n{GREEN}No data recorded yet! Generate data using Option 1 first.{RESET}")
            else:
                print(f"\n{WHITE}┌──────────────┬──────────────────┬────────────────┬─────────┐")
                print(f"│ Dataset Size │ Sequential (sec) │ Parallel (sec) │ Speedup │")
                print(f"├──────────────┼──────────────────┼────────────────┼─────────┤")
                for res in global_benchmark_history:
                    size_str = f"{res['size']:,}"
                    seq_str = f"{res['seq_time']:.4f}"
                    par_str = f"{res['par_time']:.4f}"
                    spd_str = f"{res['speedup']:.2f}x"
                    
                    print(f"│ {GREEN}{size_str:<12}{WHITE} │ {GREEN}{seq_str:<16}{WHITE} │ {GREEN}{par_str:<14}{WHITE} │ {GREEN}{spd_str:<7}{WHITE} │")
                print(f"└──────────────┴──────────────────┴────────────────┴─────────┘")
                print(f"\n{GREEN}Results loaded & saved to results/performance_results.csv{RESET}")
                
            input(f"\n{WHITE}Press Enter to return to menu...{RESET}")
            
        elif choice == '6':
            exit_program()
        else:
            print(f"{WHITE}Invalid choice. Please select between 1 and 6.{RESET}")
            time.sleep(1)

if __name__ == '__main__':
    main()