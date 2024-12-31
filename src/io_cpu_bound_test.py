import threading
import multiprocessing
import os
import time

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def cpu_task(process_id):
    print(f"Process {process_id} running on CPU core: {os.sched_getaffinity(0)}")
    start_time = time.time()
    print(f"Process {process_id} starting CPU operation")
    result = fibonacci(35)  # Computationally intensive
    cpu_duration = time.time() - start_time
    print(f"Process {process_id} computed fibonacci(35)={result} in {cpu_duration:.2f} seconds")

def io_task(thread_id):
    print(f"Thread {thread_id} running on CPU core: {os.sched_getaffinity(0)}")
    start_time = time.time()
    print(f"Thread {thread_id} starting I/O operation")
    time.sleep(2)
    io_duration = time.time() - start_time
    print(f"Thread {thread_id} completed I/O in {io_duration:.2f} seconds")

# Create and start processes for CPU-bound tasks
processes = []
for i in range(os.cpu_count()):  # Use number of CPU cores
    process = multiprocessing.Process(target=cpu_task, args=(i,))
    processes.append(process)
    process.start()

# Create and start threads for I/O-bound tasks
threads = []
for i in range(20):
    thread = threading.Thread(target=io_task, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all processes to complete
for process in processes:
    process.join()

# Wait for all threads to complete
for thread in threads:
    thread.join()
