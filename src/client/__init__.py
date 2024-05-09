import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from client.client import ClientUDP, ClientRawUDP