import socket
import ifaddr
ipwhitelisting=False
domain = "http://localhost:8000/"
server_ip = socket.gethostbyname(socket.gethostname())
merchant_check=True