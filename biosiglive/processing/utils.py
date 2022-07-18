"""
This file is part of biosiglive. It contains classes to help data processing.
"""

import numpy as np

class NumpyQueue:
    
    def __init__(self, max_size=1000, queue=np.array([[],[]])):
        """
        Initialize the NumpyQueue Class FIFO style.
        """
        self.max_size = max_size
        self.queue = queue

    def enqueue(self, item):
        """
        Enqueue numpy array at the end of the queue.
        If we go over the max_size, we trim it down.
        """
        self.queue = np.append(self.queue, item, axis=1)
        if self.queue.shape[1] > self.max_size:
            self.dequeue(n_samples=self.queue.shape[1]-self.max_size)

    def dequeue(self, n_samples=1):
        """
        Dequeue numpy array from the front of the queue.
        If the queue has less values than max_size-n_samples to remove,
        it means that we are at a deficit, so include zeros to make up the missing data.
        """
        pop = self.queue[:,:n_samples]
        self.queue = np.delete(self.queue, range(n_samples), axis=1)
        if self.queue.shape[1] < self.max_size-n_samples:
            self.queue = np.append(self.queue, np.zeros((self.queue.shape[0], self.max_size-self.queue.shape[1])), axis=1)
            
        return pop


