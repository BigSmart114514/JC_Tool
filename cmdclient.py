import socket



print("""Microshoot Windos [版本 114.514.191.9.810]
(c) 2085 Microshoot Cooperation. 保留部分权利。
(c) Dehou Studio 保留部分权利。
Pydon 1.1.9  [MSC v.2816 96 bit (AMB96)] on win48""")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('172.16.11.15', 10001)
sock.connect(server_address)
command=input(">")
sock.sendall(len(command.encode("utf-8")).to_bytes(4, byteorder='big'))
sock.sendall(command.encode("utf-8"))
data_length=sock.recv(4)
byte_arr = b''
while len(byte_arr) < int.from_bytes(data_length, byteorder='big'):
    packet = sock.recv(4096)
    if not packet:
        break
    byte_arr += packet
print(byte_arr.decode("utf-8"))
