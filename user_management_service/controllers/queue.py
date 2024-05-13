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
