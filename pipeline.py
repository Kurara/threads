import random 
import threading
import logging
import queue


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
stream.setFormatter(logging.Formatter(
    "%(asctime)s: %(message)s"
))

logger.addHandler(stream)


class ThreadPipeline:

    SENTINEL = object()

    def producer(pipeline):
        """Pretend we're getting a message from the network."""
        for index in range(10):
            message = random.randint(1, 101)
            logger.info("Producer got message: %s", message)
            pipeline.set_message(message, "Producer")

        # Send a sentinel message to tell consumer we're done
        pipeline.set_message(SENTINEL, "Producer")


    def consumer(pipeline):
        """Pretend we're saving a number in the database."""
        message = 0
        while message is not SENTINEL:
            message = pipeline.get_message("Consumer")
            if message is not SENTINEL:
                logger.info("Consumer storing message: %s", message)


class EventPipeline:
    
    SENTINEL = object()

    def producer(pipeline, event):
        """Pretend we're getting a message from the network."""
        while not event.is_set():
            message = random.randint(1, 101)
            logger.info("Producer got message: %s", message)
            pipeline.set_message(message, "Producer")

        logger.info("Producer received EXIT event. Exiting")

    def consumer(pipeline, event):
        """Pretend we're saving a number in the database."""
        while not event.is_set() or not pipeline.empty():
            message = pipeline.get_message("Consumer")
            logger.info(
                "Consumer storing message: %s  (queue size=%s)",
                message,
                pipeline.qsize(),
            )

        logger.info("Consumer received EXIT event. Exiting")


class PipelineOld:
    """
    Class to allow a single element pipeline between producer and consumer.
    """
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self, name):
        logger.debug("%s:about to acquire getlock", name)
        self.consumer_lock.acquire()
        logger.debug("%s:have getlock", name)
        message = self.message
        logger.debug("%s:about to release setlock", name)
        self.producer_lock.release()
        logger.debug("%s:setlock released", name)
        return message

    def set_message(self, message, name):
        logger.debug("%s:about to acquire setlock", name)
        self.producer_lock.acquire()
        logger.debug("%s:have setlock", name)
        self.message = message
        logger.debug("%s:about to release getlock", name)
        self.consumer_lock.release()
        logger.debug("%s:getlock released", name)

class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        logging.debug("%s:about to get from queue", name)
        value = self.get()
        logging.debug("%s:got %d from queue", name, value)
        return value

    def set_message(self, value, name):
        logging.debug("%s:about to add %d to queue", name, value)
        self.put(value)
        logging.debug("%s:added %d to queue", name, value)