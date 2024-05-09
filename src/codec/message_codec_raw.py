'''
Gustavo Montenegro Maia Chaves - 20200015824
Lucas Gomes Dantas - 20200082925
Mayra Daher De Carvalho Pereira - 20190031238
'''

from socket import inet_aton, gethostbyname, gethostname, IPPROTO_UDP
from codec_template.message_codec_template import CodecTemplate
from struct import pack


class CodecRaw(CodecTemplate):
    
    def _wrapround(self, checksum):
        # Verifica se o checksum é maior que 16
        while checksum > 0xFFFF:
            # Aplica um and entre o valor e 16
            lower_16_bits = checksum & 0xFFFF
            # Move os bits excedentes para a direita para formar o carry
            carry = checksum >> 16
            checksum = lower_16_bits + carry
        
        return checksum

    def _calculate_checksum(self, data: bytes) -> int:
        if len(data) % 2 == 1:
            data += b'\x00'  # Adiciona um byte zero se o comprimento dos dados for ímpar

        per_sume = 0
        # Quebra os dados em pares de 2 bytes e soma todos os valores usando um loop for tradicional
        
        for i in range(0, len(data), 2):
            segment = int.from_bytes(data[i:i+2], 'big')
            per_sume += segment
            
        # Aplica o wrapround para garantir que está dentro de 16 bits
        per_sume = self._wrapround(per_sume)

        # Executa o complemento de um sobre o resultado
        return ~per_sume & 0xFFFF
    
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
        
        #   UDP header
        udp_length = 8 + len(message_bytes)
        udp_header = pack('!HHHH', 6543, 50000, udp_length, 0)

        # Pseudo header para cálculo do checksum
        src_ip_bytes = inet_aton(gethostbyname(gethostname()))
        dst_ip_bytes = inet_aton('15.228.191.109')
        placeholder = 0
        protocol = IPPROTO_UDP # 17
        pseudo_header = pack('!4s4sBBH', src_ip_bytes, dst_ip_bytes, placeholder, protocol, udp_length)
        datagrama = pseudo_header + udp_header + message_bytes
        
        # Calcula checksum
        checksum = self._calculate_checksum(datagrama)
        
        # Atualiza UDP Header
        udp_header = pack('!HHHH', 6543, 50000, udp_length, checksum)
        
        # Gera pacote codificado para envio
        packet = udp_header + message_bytes

        return packet

    def decode(self, message_bytes: bytes) -> str:
        # Seleciona as informações da mensagem
        data = message_bytes[28:]
        
        # Converter bytes para string binária
        binary_strings = []
        for byte in data:
            binary_strings.append(format(byte, '08b'))
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

        # Iteração em intervalos de 8 bytes até leitura completa da mensagem
        for i in range(32, 32 + len_response * 8, 8):
            byte_bin = bin_message[i:i + 8]
            byte_int = int(byte_bin, 2)
            bytes_response.append(byte_int)

        # Trata strings (escolha do usuário foi data ou motivação)
        if msg_type in [0, 1]:
            message_response = []
            for byte in bytes_response:
                char = chr(byte)
                message_response.append(char)
            message_response_str = ''.join(message_response)
        # Trata número (quantidade de requisições)
        else:
            num = 0
            for i, byte in enumerate(bytes_response[::-1]):  # Inverte a lista (LSB)
                num += byte * 256**i
            message_response_str = str(num)
        
        return message_response_str
