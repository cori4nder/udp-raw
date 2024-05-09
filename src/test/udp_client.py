import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from client import ClientUDP
from codec.message_codec import Codec

client_udp = ClientUDP(codec=Codec(), server_address='15.228.191.109', server_port=50000)

client_udp.run()
