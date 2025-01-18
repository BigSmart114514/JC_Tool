import socket
from time import sleep
#from PIL import Image, ImageGrab
#import io
#import subprocess
#import datetime,os
from subprocess import Popen,PIPE
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

def Get_current_path():
    process = Popen(
        "cd",stdout=PIPE, stderr=PIPE, shell=True
    )
    output,error = process.communicate()
    return output.decode("GBK")
def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

#current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#file_name = f"log {current_time}.txt"
def run_command(cmd,directory):
    global path
    command_list=str(cmd).split()
    
    if cmd=="exit":
        return "","无法退出JC server",0
    if (command_list[0]=="cd" and len(command_list)>1):
        '''if (command_list[1]=="\\"):
            path=path.capitalize()
            print(path)
            return "","",0'''
        if (command_list[1]=="..\\"):
            path_list=path.split("\\")
            path_list.pop()
            path="\\".join(path_list)
            return "","",0
        else:
            try:
                try:
                    index_using_index = command_list[1].index(":")
                    path=command_list[1]
                except ValueError:
                    if (command_list[1].endswith('\\')):
                        path=path+command_list[1]
                    else:
                        path=path+"\\"+command_list[1]
                process = Popen(
                "cd",cwd=path,stdout=PIPE, stderr=PIPE, shell=True
                )
                output,error = process.communicate()
                path=str(output.decode("GBK")).strip()
                return "","",0
            except:
                path=directory
                
                return "","系统找不到指定的路径。",0
    else:
        process = Popen(
            cmd, cwd=directory,stdout=PIPE, stderr=PIPE, shell=True
        )
        output, error = process.communicate()
        return output.decode("GBK"), error.decode("GBK"), process.returncode


addr=getip()
port=10001
def serve():
    global path
    
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (addr, port)
    sock.bind(server_address)

    # 监听传入连接
    sock.listen(1)

    try:
        
        connection, client_address = sock.accept()
        

        
        
        command=recv_sock(connection)
        print("command:",command)
        
        path=recv_sock(connection)
        print(path)


        output,error,code=run_command(command,path)
        print(output,error)
        connection.sendall(len(output.encode("utf-8")).to_bytes(4, byteorder='big'))
        connection.sendall(output.encode("utf-8"))
        sleep(0.1)
        connection.sendall(len(error.encode("utf-8")).to_bytes(4, byteorder='big'))
        connection.sendall(error.encode("utf-8"))
        sleep(0.1)
        connection.sendall(len(path.encode("utf-8")).to_bytes(4, byteorder='big'))
        connection.sendall(path.encode("utf-8"))
        
        
        

                
        
        

       
    finally:
        
        sock.close()

#path=str(Get_current_path()).strip()
while True:
    try:
        serve()
    except Exception as e:
        pass
