import threading
import logging
import time


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)

logger.addHandler(stream)


class BaseThreading:
    def print_cube(num): 
        """ 
        function to print cube of given num 
        """
        print("Cube: {}\n".format(num * num * num)) 
    
    def print_square(num): 
        """ 
        function to print square of given num 
        """
        print("Square: {}\n".format(num * num)) 
    
    def thread_function(name):
        import os

        logger.info("ID of process running task: {}".format(os.getpid()))
        logger.info("Thread %s: starting", name)
        time.sleep(20)
        logger.info("Thread %s: finishing", name)


class RaceThreading:
  
    # global variable x 
    def __init__(self):
        self.x = 0
    
    def increment(self): 
        """ 
        function to increment global variable x 
        """
        self.x += 1
    
    def thread_task(self): 
        """ 
        task for thread 
        calls increment function 100000 times. 
        """
        for _ in range(100000): 
            self.increment() 

    def thread_task_with_lock(self, lock): 
        """ 
        task for thread 
        calls increment function 100000 times. 
        """
        lock.acquire() 
        for _ in range(100000): 
            self.increment() 
        lock.release() 