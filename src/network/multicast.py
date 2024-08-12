import logging
import socket
import struct

logger = logging.Logger("multicast", 0)


def start_multicast_receiver(multicast_group='224.3.29.71', server_address=('', 10000), response_builder=lambda: "ACK"):
    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the server address
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        logger.debug('waiting to receive message')
        data, address = sock.recvfrom(1024)

        logger.debug('received %s bytes from %s' % (len(data), address))
        logger.debug(data)
        yield data.decode('utf-8')

        logger.debug('sending acknowledgement to', address)
        sock.sendto(response_builder().encode('utf-8'), address)


def send_multicast_message(message, multicast_group=('224.3.29.71', 10000)):
    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(0.2)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    try:

        # Send data to the multicast group
        logger.debug('sending "%s"' % message)
        message_data = message.encode('utf-8')
        sock.sendto(message_data, multicast_group)

    finally:
        logger.debug('closing socket')
        sock.close()
