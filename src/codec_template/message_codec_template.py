'''
Gustavo Montenegro Maia Chaves - 20200015824
Lucas Gomes Dantas - 20200082925
Mayra Daher De Carvalho Pereira - 20190031238
'''

from abc import ABC, abstractmethod


class CodecTemplate(ABC):
    @abstractmethod
    def encode(self, msg_type: int, id: int) -> bytes:
        """
        Método para codificar uma mensagem.
        """
        pass

    @abstractmethod
    def decode(self, message_bytes: bytes) -> str:
        """
        Método para decodificar uma mensagem.
        """
        pass
