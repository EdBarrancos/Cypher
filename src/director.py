import socket
import functools
import select
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(bytes(
        f"DIRECTOR",
        "utf-8"))

    print("character_name:lang:message")

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
                    s.send(bytes(f"{message}", 'utf-8'))
                except:
                    continue