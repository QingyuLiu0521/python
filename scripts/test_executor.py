from time import time
from concurrent.futures import ProcessPoolExecutor

def cpu_bound(number):
    print(sum(i * i for i in range(number)))

def calculate_sum_without_executor(numbers):
    start = time()
    for n in numbers:
        cpu_bound(n)
    print(f"Total time (without executor): {time() - start:.2f} seconds")

def calculate_sum_with_executor(numbers):
    start = time()
    with ProcessPoolExecutor(max_workers = 16) as executor:
        results = executor.map(cpu_bound, numbers)
    print(f"Total time (with executor): {time() - start:.2f} seconds")

def main():
    numbers = [10000000 + n for n in range(4)]
    
    calculate_sum_without_executor(numbers)    # 正常单线程
    print()
    calculate_sum_with_executor(numbers)       # 多进程
    

if __name__ == '__main__':
    main()
