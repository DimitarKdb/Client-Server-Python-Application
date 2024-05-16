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
    leftQueue = Queue()
    leftThread = threading.Thread(target=lambda: parallelQuicksort(left, leftQueue))
    
    rightQueue = Queue()
    rightThread = threading.Thread(target=lambda: parallelQuicksort(right, rightQueue))

    # Start the threads
    leftThread.start()
    rightThread.start()

    # Wait for threads to finish and collect the sorted sub-arrays
    leftThread.join()
    rightThread.join()

    # Retrieve the sorted sub-arrays from threads
    leftSortedArray = leftQueue.get()
    rightSortedArray = rightQueue.get()
    
    queue.put(leftSortedArray + middle + rightSortedArray)
