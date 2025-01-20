from socket import AF_INET,socket,SOCK_DGRAM

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
def getip():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]