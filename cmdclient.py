from socket import SOCK_STREAM,AF_INET,socket
from time import sleep
from os import system
def recv_sock(connection):
    data_length = connection.recv(4)
    if not data_length:
        return
        # 接收数据
    byte_arr = b''
    while len(byte_arr) < int.from_bytes(data_length, byteorder='big'):
        packet = connection.recv(4096)
        if not packet:
            break
        byte_arr += packet
    return byte_arr.decode("utf-8")
ADDR='172.16.11.15'
PORT=10001

system("cls")
system("title JC client(unconnected)")

print("""Microshoot Windos [版本 114.514.191.9.810]
(c) 2085 Microshoot Cooperation. 保留部分权利。
(c) Dehou Studio 保留部分权利。
Pydon 1.1.9  [MSC v.2816 96 bit (AMB96)] on win48""")

path="C:\\Users\\Administrator"

while True:
    command=input(path+">")
    sock = socket(AF_INET, SOCK_STREAM)
    server_address = (ADDR,PORT )
    sock.connect(server_address)
    system(f"title JC client({ADDR}:{PORT})")
    print("connected to JC server!!")


    sock.sendall(len(command.encode("utf-8")).to_bytes(4, byteorder='big'))
    sock.sendall(command.encode("utf-8"))
    sleep(0.1)
    sock.sendall(len(path.encode("utf-8")).to_bytes(4 , byteorder="big"))
    sock.sendall(path.encode("utf-8"))

    print(recv_sock(sock))

    print("error:",recv_sock(sock))
    path=recv_sock(sock)
    sock.close

#print("path:",recv_sock(sock))
