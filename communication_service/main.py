from communication_service import consul_client, hz_config, hz_client
from communication_service.controllers.queue import QueueReader
from communication_service.services.communication import CommunicationService
import sys
import threading
# import atexit

def exit_handler():
    consul_client.agent.service.deregister(service_id)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        service_num = sys.argv[1]
    else:
        raise ValueError("Please provide a service number.")

    # atexit.register(exit_handler)

    service_id = f"communication_service_{service_num}"
    consul_client.agent.service.register(f"communication_service", port=6100+int(service_num), service_id=service_id)

    print("HERERERERE")
    communication = CommunicationService(QueueReader(hz_client.get_queue(hz_config["message_queue"]).blocking()))
    threading.Thread(target=communication.start).start()

    while True:
        communication.parse_memory()
