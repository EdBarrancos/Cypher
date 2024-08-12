from network.helpers import get_host, next_free_port
from network.multicast import start_multicast_receiver, send_multicast_message


def start_receiver_thread():
    for s in start_multicast_receiver():
        
        print(s)


def find_host_and_connect():
    message = f'CLI:{get_host()}:{next_free_port()}'
    send_multicast_message(message)
