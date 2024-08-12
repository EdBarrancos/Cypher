import socket
import functools
import select
import sys

from  config_handler import Configutations

class ClientConfigurations(Configutations):
    pass


name = input("Your character name: ")
languages = input("Which languages do you speak? (Separate with ,): ")\
                .replace(" ", "").split(',')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    config = ClientConfigurations("config/config.ini")
    s.connect((config.get_server_ip(), config.get_server_port()))
    s.send(bytes(
        f"{name}:{functools.reduce(lambda a, b: a + ',' + b, languages)}",
        "utf-8"))

    print("lang:message")

    while True:
        sockets_list = [sys.stdin, s] 

        read_sockets,write_socket, error_socket = select.select(
            sockets_list,[],[])
        
        for sock in read_sockets:
            if sock == s:
                message = s.recv(2048).decode('utf-8')
                print(message)
            else:
                try:
                    message = sys.stdin.readline()
                    if message == "exit":
                        s.close()
                        break
                    # TODO: Check if player speaks lang
                    # TODO: Check if formatting is correct
                    s.send(bytes(f"{message}", 'utf-8'))
                except:
                    continue