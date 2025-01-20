#from time import sleep
from socket import socket,SOCK_DGRAM,AF_INET,SOCK_STREAM
#from subprocess import Popen,PIPE
from os import path,listdir
from json import dumps
from pubilc_functions import recv_sock,getip
def list_files(directory):
    try:
        files=[]
        for file in listdir(directory):
            full_path = path.join(directory, file)
            if path.isfile(full_path):
                #print(f"{file} (文件)")
                files.append([file,f"{file.split('.')[-1]}文件"])
            elif path.isdir(full_path):
                #print(f"{file} (文件夹)")
                files.append([file,"<dir>"])

        return files
    except Exception as e:
        print(e)
        return [["拒绝访问","error"]]
ADDR=getip()
PORT=10002
def serve():
    
    
    sock = socket(AF_INET, SOCK_STREAM)
    server_address = (ADDR, PORT)
    sock.bind(server_address)

    # 监听传入连接
    sock.listen(1)

    try:
        
        connection, client_address = sock.accept()
        path=recv_sock(connection)
        files=list_files(path)
        files=dumps(files).encode("utf-8")
        connection.sendall(len(files).to_bytes(4, byteorder='big'))
        connection.sendall(files)
        
    finally:
        
        sock.close()
while True:
    try:
        serve()
    except Exception as e:
        pass
