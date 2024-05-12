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

class QueueWriter:
    """
    A class that writes messages to a queue.

    Attributes:
        queue (Queue): The Hazelcast queue object to which messages are written.
    """

    def __init__(self, queue):
        self.queue = queue

    def write_queue(self, message):
        """
        Writes a message to the Hazelcast queue.

        Args:
            message (str): The message to be written to the queue.
        """
        while True:
            result = self.queue.offer(message)
            if result:
                print(f"{message} has been written to the queue")
                break
            else:
                print(f"Failed to write {message} to the queue. Retrying...")
