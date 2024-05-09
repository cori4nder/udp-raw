'''
Gustavo Montenegro Maia Chaves - 20200015824
Lucas Gomes Dantas - 20200082925
Mayra Daher De Carvalho Pereira - 20190031238
'''

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from client import ClientRawUDP
from codec.message_codec_raw import CodecRaw

client_udp = ClientRawUDP(codec=CodecRaw(), server_address='15.228.191.109', server_port=50000)

client_udp.run()
