import socket
from dataclasses import dataclass
from _thread import *
import configparser



# TODO: Multicast IP
# TODO: Ability to narrate

@dataclass
class Player:
    conn: socket
    addr: any
    name: str
    languages: list

    def speaks_language(self, language):
        return language in self.languages
    
class Server:
    def __init__(self) -> None:
        self.list_of_clients = []
        self.director = None

        configs = Server.read_config()
        IP = configs["ip"]
        PORT = configs["port"]

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((IP, PORT))
        self.server.listen(100)

        print("Server Up and Running")
    
    def read_config():
        config = configparser.ConfigParser()
 
        config.read('config/config.ini')
    
        socket_ip = config.getboolean('Socket', 'SERVER_IP')
        socekt_port = config.get('Socket', 'SERVER_PORT')
    
        config_values = {
            'ip': socket_ip,
            'port': socekt_port
        }
    
        return config_values

    def run(self):
        while True:
            conn, addr = self.server.accept()
            print(f"Connected by {addr}")
            # name:lang1,lang2...
            authentication = conn.recv(2048).decode("utf-8")
            if authentication == "DIRECTOR":
                director = conn
                start_new_thread(self.handle_director, (conn,))
                continue
            new_player = Player(
                conn, 
                addr, 
                authentication.split(':')[0], 
                authentication.split(':')[1].split(','))

            self.list_of_clients.append(new_player)
            start_new_thread(self.handle_client, (new_player,))
    
    def remove_player(self, player):
        if player in self.list_of_clients:
            self.list_of_clients.remove(player) 

    def handle_client(self, player: Player):
        print(f"{player.name} Logged in")
        
        while True:
            try:
                message = player.conn.recv(2048)
                if not message:
                    self.remove_player(player)
                    return
                
                message = message.decode('utf-8')
                # language:message
                
                print(f"< {player.name},{message.split(':')[0]} > " +
                        f"{message.split(':')[1][:-1]}")
                
                self.broadcast(player.name, message.split(':')[0], message.split(':')[1][:-1])
            except:
                continue

    def handle_director(self, conn: socket):
        print(f"Director Logged in")

        while True:
            try:
                message = conn.recv(2048)
                if not message:
                    return
                
                message = message.decode('utf-8')
                # character:language:message
                
                print(f"< DIRECTOR,{message.split(':')[0]},{message.split(':')[1]} > " +
                        f"{message.split(':')[2][:-1]}")
                
                self.broadcast(message.split(':')[0], message.split(':')[1], message.split(':')[2][:-1])
            except:
                continue


    def broadcast(self, sender_name, language, message):
        # TODO: Make this more uniform so it works well on player and dm
        to_remove = []
        is_director = True
        for player in self.list_of_clients:
            if player.name == sender_name:
                is_director = False
                continue
            try:
                Server.send_message(sender_name, player, language, message)
            except:
                player.conn.close()
                to_remove.append(player)
        
        for p in to_remove:
            self.remove_player(p)

        if not is_director:
            Server.send_message_director(sender_name, self.director, language, message)

    def send_message_director(sender_name, conn: socket, language, message):
        conn.send(bytes(
            f"{sender_name}:{language}:{message}",
            'utf-8'))

    def send_message(sender_name, reciver: Player, language, message):
        if reciver.speaks_language(language):
            reciver.conn.send(bytes(
                f"{sender_name}:{language}:{message}",
                'utf-8'))
            return
        reciver.conn.send(bytes(
            f"{sender_name}:{language}:{Server.randomize_message(message)}",
            'utf-8'))

    def randomize_message(message: str):
        return "".join(map(lambda a: ' ' if a == ' ' else '?', message))
    
if __name__ == "__main__":
    server = Server()
    server.run()