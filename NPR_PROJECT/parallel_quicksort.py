import threading
from queue import Queue

def parallelQuicksort(arr, queue):
    if len(arr) <= 1:
        queue.put(arr)
        return
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Create thread objects for sorting left and right sub-arrays
    left_queue = Queue()
    left_thread = threading.Thread(target=lambda: parallelQuicksort(left, left_queue))
    
    right_queue = Queue()
    right_thread = threading.Thread(target=lambda: parallelQuicksort(right, right_queue))

    # Start the threads
    left_thread.start()
    right_thread.start()

    # Wait for threads to finish and collect the sorted sub-arrays
    left_thread.join()
    right_thread.join()

    # Retrieve the sorted sub-arrays from threads
    left_sorted = left_queue.get()
    right_sorted = right_queue.get()
    
    queue.put(left_sorted + middle + right_sorted)
