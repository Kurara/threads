import unittest
from main import BaseThreading, RaceThreading
import logging
import threading 


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
stream.setFormatter(logging.Formatter(
    "%(asctime)s: %(message)s"
))

logger.addHandler(stream)


class ThreadsText(unittest.TestCase):

    def test_basic_thread(self):
        # creating thread 
        t1 = threading.Thread(
            target=BaseThreading.print_square, args=(10,), daemon=True
        ) 
        t2 = threading.Thread(
            target=BaseThreading.print_cube, args=(10,)
        ) 
    
        logger.info("starting thread 1...")
        t1.start() 
        logger.info("starting thread 2...") 
        t2.start() 
    
        logger.debug("wait until thread 1 is completely executed")
        t1.join() 
        logger.debug("wait until thread 2 is completely executed")
        t2.join() 

        logger.info("Done!")

    def test_multiple_threads(self):
        threads = list()
        for index in range(3):
            logger.info("Main    : create and start thread %d.", index)
            x = threading.Thread(target=BaseThreading.thread_function, args=(index,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            logger.info("Main    : before joining thread %d.", index)
            thread.join()
            logger.info("Main    : thread %d done", index)

    def test_multiple_threads_op2(self):
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(BaseThreading.thread_function, range(3))

    def test_memory_access(self):
        thread_manager = RaceThreading()
        for i in range(10): 
            # creating threads 
            t1 = threading.Thread(target=thread_manager.thread_task) 
            t2 = threading.Thread(target=thread_manager.thread_task) 
        
            # start threads 
            t1.start() 
            t2.start() 
        
            # wait until threads finish their job 
            t1.join() 
            t2.join() 

            logger.info("Iteration {0}: x = {1}".format(i,thread_manager.x))

    def test_memory_access_with_lock(self):
        thread_manager = RaceThreading()
        for i in range(10): 
            # creating a lock 
            lock = threading.Lock() 
        
            # creating threads 
            t1 = threading.Thread(target=thread_manager.thread_task_with_lock, args=(lock,)) 
            t2 = threading.Thread(target=thread_manager.thread_task_with_lock, args=(lock,)) 
        
            # start threads 
            t1.start() 
            t2.start() 
        
            # wait until threads finish their job 
            t1.join() 
            t2.join() 

            logger.info("Iteration {0}: x = {1}".format(i,thread_manager.x))

    def test_pipeline(self):
        from pipeline import ThreadPipeline, Pipeline
        import concurrent.futures

        pipeline = Pipeline()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(ThreadPipeline.producer, pipeline)
            executor.submit(ThreadPipeline.consumer, pipeline)

    def test_event(self):
        from pipeline import EventPipeline, Pipeline
        import concurrent.futures

        pipeline = Pipeline()
        event = threading.Event()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(EventPipeline.producer, pipeline, event)
            executor.submit(EventPipeline.consumer, pipeline, event)

            time.sleep(0.1)
            logging.info("Main: about to set event")
            event.set()