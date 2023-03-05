import multiprocessing
import signal
import time
from multiprocessing import Queue

def timeout_handler(signum, frame):
    raise TimeoutError("The worker function took too long and timed out")

def worker_function_1(queue, identity, attempt):
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(18)
        # Your code that might raise an exception goes here
        print(f"Running worker function 1, attempt {attempt}")
        time.sleep(15)
        result = "Function 1 succeeded."
        queue.put((identity, result))
        print("Worker function 1 completed successfully")
        signal.alarm(0)
    except Exception as e:
        if attempt < 3:
            print(f"Worker function 1 raised an exception: {e}. Retrying...")
            worker_function_1(queue, identity,  attempt + 1)
        else:
            print(f"Worker function 1 raised an exception: {e}. Giving up after 3 attempts.")

            result = "Function 1 failed."
            queue.put((identity, result))
    

def worker_function_2(queue,identity,  attempt):
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(5)
        # Your code that might raise an exception goes here
        print(f"Running worker function 2, attempt {attempt}")
        time.sleep(4)
        result = "Function 2 succeeded."
        queue.put((identity, result))
        print("Worker function 2 completed successfully")
        signal.alarm(0)
    except Exception as e:
        if attempt < 3:
            print(f"Worker function 2 raised an exception: {e}. Retrying...")
            worker_function_2(queue, identity, attempt + 1)
        else:
            print(f"Worker function 2 raised an exception: {e}. Giving up after 3 attempts.")
            result = "Function 2 failed."
            queue.put((identity, result))


if __name__ == '__main__':
    queue = Queue()
    process_1 = multiprocessing.Process(target=worker_function_1, args=(queue, 'function_1', 1))
    process_2 = multiprocessing.Process(target=worker_function_2, args=(queue, 'function_2', 1))
    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()

    results = []
    while True:
        if not queue.empty():
            results.append(queue.get())
            print(results)

        if len(results) == 2:
            break

    print(results)
