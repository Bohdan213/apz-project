class QueueReader:
    """
    A class that reads messages from a queue and stores them in memory.

    Attributes:
        memory (list): A list to store the messages read from the queue.
        queue (Queue): The Hazelcast queue object from which messages are read.
    """

    def __init__(self, queue):
        self.memory = []
        self.queue = queue

    def read_queue(self):
        """
        Continuously reads messages from the Hazelcast queue and stores them in memory.

        This method runs in an infinite loop and appends each message taken from the queue
        to the memory list. It also prints a message indicating the last message written
        to memory.
        """
        while True:
            self.memory.extend(self.queue.take())
            print(f"{self.memory[-1]} has been written to memory")
