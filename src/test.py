import threading
import time

def cpu_bound_task():
    count = 0
    for _ in range(10000000):
        count += 1

def gil_example():
    print("Starting GIL example...")
    
    # Create two threads
    start_time = time.time()
    thread1 = threading.Thread(target=cpu_bound_task)
    thread2 = threading.Thread(target=cpu_bound_task)
    
    # Start both threads
    thread1.start()
    thread2.start()
    
    # Wait for both to finish
    thread1.join()
    thread2.join()
    
    end_time = time.time()
    print(f"Two threads took: {end_time - start_time:.2f} seconds")
    
    # Now run sequentially
    start_time = time.time()
    cpu_bound_task()
    cpu_bound_task()
    end_time = time.time()
    print(f"Sequential took: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    gil_example()
