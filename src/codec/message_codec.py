'''
Gustavo Montenegro Maia Chaves - 20200015824
Lucas Gomes Dantas - 20200082925
Mayra Daher De Carvalho Pereira - 20190031238
'''

from codec_template.message_codec_template import CodecTemplate


class Codec(CodecTemplate):
    def encode(self, msg_type: int, id: int) -> bytes:
        # Converter valores para strings binárias
        req_bin = format(0, '04b')
        msg_type_bin = format(msg_type, '04b')
        id_bin = format(id, '016b')

        # Combinar tudo em uma única string binária
        message_bin = req_bin + msg_type_bin + id_bin

        # Lista para armazenar os bytes
        message_bytes_list = []

        for i in range(0, len(message_bin), 8):
            # Segmento de 8 bits
            byte_bin = message_bin[i:i + 8]

            # Segmento binário para int
            byte_int = int(byte_bin, 2)

            message_bytes_list.append(byte_int)

        # Lista de int para sequência de bytes
        message_bytes = bytes(message_bytes_list)

        return message_bytes

    def decode(self, message_bytes: bytes) -> str:
        # Converter bytes para string binária
        binary_strings = []

        for byte in message_bytes:
            binary_strings.append(format(byte, '08b'))

        # String única
        bin_message = ''.join(binary_strings)

        # Decodificar tipo da mensagem
        msg_type = int(bin_message[4:8], 2)
        
        # Caso receba mensagem inválida
        if msg_type == 3:
            print("Servidor informa: Requisição inválida!!!")
            print("PS.: Se o senhor estiver lendo essa mensagem tente novamente umas 5 vezes, juro que de vez em quando pega")
            raise ValueError("Servidor informa: Requisição inválida!!!", msg_type)

        # Tamanho da resposta
        len_response = int(bin_message[24:32], 2)

        # Decodificar bytes de resposta
        bytes_response = []

        for i in range(32, 32 + len_response * 8, 8):
            byte_bin = bin_message[i:i + 8]
            byte_int = int(byte_bin, 2)
            bytes_response.append(byte_int)

        # Trata strings (escolha foi data ou motivação)
        if msg_type in [0, 1]:
            message_response = []

            for byte in bytes_response:
                char = chr(byte)
                message_response.append(char)

            message_response_str = ''.join(message_response)
        # Trata número (escolha foi qtd de requisições)
        else:
            num = 0
            for i, byte in enumerate(bytes_response[::-1]):  # Inverte a lista (LSB)
                num += byte * 256**i
            message_response_str = str(num)

        return message_response_str
