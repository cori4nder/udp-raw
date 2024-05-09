import os
from random import randint
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_RAW, IPPROTO_UDP

from codec_template.message_codec_template import CodecTemplate


class Client():
    def __init__(self, codec: CodecTemplate, server_address: str='15.228.191.109', server_port: int=50000):
        """
        Inicializa um objeto Cliente.

        Args:
            codec (CodecTemplate): O codec utilizado para codificar e decodificar mensagens.
            server_address (str): O endereço IP do servidor remoto. Padrão é '15.228.191.109'.
            server_port (int): A porta do servidor remoto. Padrão é 50000.
        """
        self.codec = codec
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = socket(AF_INET, SOCK_DGRAM)

    def show_menu(self):
        """
        Exibe o menu de opções para o cliente.
        """
        width = 80
        print("")
        print("*" * width)
        print("{:^{width}}".format("CLIENTE UDP", width=width))
        print("*" * width)
        print("{:<3}{:>{width}}".format("[1]", "Data e hora atual", width=width - 3))
        print("{:<3}{:>{width}}".format("[2]", "Uma mensagem motivacional", width=width - 3))
        print("{:<3}{:>{width}}".format("[3]", "Quantidade de respostas emitidas", width=width - 3))
        print("{:<3}{:>{width}}".format("[4]", "Sair", width=width - 3))
        print("*" * width)
        print("")

    def run(self):
        """
        Executa o cliente, exibindo o menu e processando a escolha do usuário.
        """
        while True:
            self.show_menu()
            choice = int(input("Escolha uma opção: "))
            print("")

            if choice not in range(1, 5):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Opção Inválida. Por favor, tente novamente")
                continue

            if choice == 4:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Sessão do Cliente Finalizada")
                self.client_socket.close()
                break

            self.msg_type = choice - 1
            self.id = randint(1, 65535)

            # Enviar a solicitação
            self._send_request()

            # Receber e exibir a resposta
            response_bytes = self._receive_response()
            try:
                response = self.codec.decode(response_bytes)
            except Exception as e:
                print(e)
                print("EXIT EXECUTADO PORQUE EM CASO DE CONTINUE DO WHILE EM REQUISIÇÕES INVÁLIDAS DO SERVIDOR OCORRE PROBLEMA COM OS BUFFERS DA REDE (PACOTES ANTIGOS VEM NO LUGAR DOS ATUAIS)")
                exit()
            
            print("")
            print(f'>> Resposta do Servidor: {response}')

    def _send_request(self):
        """
        Envia uma solicitação ao servidor.
        """
        raise NotImplementedError("Subclasses devem implementar _send_request.")

    def _receive_response(self):
        """
        Recebe e retorna a resposta do servidor.
        """
        raise NotImplementedError("Subclasses devem implementar _receive_response.")


class ClientUDP(Client):
    def __init__(self, codec: CodecTemplate, server_address: str, server_port: int):
        super().__init__(codec, server_address, server_port)
        self.client_socket = socket(AF_INET, SOCK_DGRAM)

    def _send_request(self):
        message = self.codec.encode(self.msg_type, self.id)
        self.client_socket.sendto(message, (self.server_address, self.server_port))

    def _receive_response(self):
        modified_message, _ = self.client_socket.recvfrom(259) # 0.5 + 0.5 + 2 + 255 = 259 bytes
        return modified_message


class ClientRawUDP(Client):
    def __init__(self, codec: CodecTemplate, server_address: str, server_port: int):
        super().__init__(codec, server_address, server_port)
        self.client_socket = socket(AF_INET, SOCK_RAW, IPPROTO_UDP)

    def _send_request(self):
        message = self.codec.encode(self.msg_type, self.id)
        self.client_socket.sendto(message, (self.server_address, self.server_port))
        
    def _receive_response(self):
        modified_message, _ = self.client_socket.recvfrom(2048)
        return modified_message
