import configparser


class Configurations:

    def __init__(self, settings_file_path) -> None:
        config = configparser.ConfigParser()

        config.read(settings_file_path)

        socket_ip = config.get('Socket', 'SERVER_IP')
        socekt_port = config.getint('Socket', 'SERVER_PORT')

        self.configuration = {
            'ip': socket_ip,
            'port': socekt_port
        }

    def get_server_ip(self) -> str:
        return self.configuration["ip"]

    def get_server_port(self) -> str:
        return self.configuration["port"]
