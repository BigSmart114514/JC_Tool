#import time
from time import sleep
from socket import socket,SOCK_DGRAM,AF_INET,SOCK_STREAM
from PIL import ImageGrab
#import io
from io import BytesIO
from pyautogui import moveTo,click,rightClick
#import pyautogui
#import datetime
from datetime import datetime
from pubilc_functions import getip
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"log {current_time}.txt"
DEBUG=True
INFO="INFO"
WARNING="WARNING"
ERROR="ERROR"
def log(status,message):
    if DEBUG:
        with open(file_name, 'a') as file:
            file.write("[{} {}] {}\n".format(datetime.now().strftime("%H:%M:%S"),status,message))

log (INFO,"file running")

def serve():

    addr=getip()
    port=10000
    log (INFO,f"socket server running on {addr}:{port}")
    sock = socket(AF_INET, SOCK_STREAM)
    server_address = (addr, port)
    sock.bind(server_address)

    # 监听传入连接
    sock.listen(1)

    try:
        log(INFO,"waiting for connection")
        connection, client_address = sock.accept()
        log(INFO,f"connection from {client_address}")
        recfps=connection.recv(4)
        fps=int.from_bytes(recfps,byteorder='big', signed=True)
        log(INFO,f"fps set to {fps}")
        try:
            while True:
                
                screenshot = ImageGrab.grab()
            
                img_byte_arr = BytesIO()
                screenshot.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                connection.sendall(b"1")
                connection.sendall(len(img_byte_arr).to_bytes(4, byteorder='big'))
                connection.sendall(img_byte_arr)
                mouseupdate=connection.recv(1)
                if (mouseupdate==b'1'):

                    recmousex=connection.recv(4)
                    recmousey=connection.recv(4)
                    mousex=int.from_bytes(recmousex, byteorder='big', signed=True)
                    mousey=int.from_bytes(recmousey, byteorder='big', signed=True)
                    moveTo(mousex, mousey)
                    click()
                    log(INFO,f"left clicking at {mousex},{mousey}")
                elif (mouseupdate==b'2'):

                    recmousex=connection.recv(4)
                    recmousey=connection.recv(4)
                    mousex=int.from_bytes(recmousex, byteorder='big', signed=True)
                    mousey=int.from_bytes(recmousey, byteorder='big', signed=True)
                    moveTo(mousex, mousey)
                    rightClick()
                    log(INFO,f"right clicking at {mousex},{mousey}")
                elif(mouseupdate==b'0'):
                    pass
                else :
                    log(WARNING,f"unsupported mouse operation from client :{mouseupdate}")
                sleep(int(fps*1.0/1000))

                '''# 接收数据
                data = connection.recv(1024)
                print(f'收到数据: {data.decode()}')

                # 发送响应
                response = '这是服务器的响应'
                connection.sendall(response.encode())
        '''
        except Exception as e:
            log(WARNING,repr(e))
        finally:
            connection.close()
            log(INFO,f"closing connection {client_address}")
    except Exception as e:
        log(WARNING,repr(e))
    finally:
        log(INFO,"closing socket")
        sock.close()
while True:
    try:
        serve()
    except Exception as e:
        log(WARNING,repr(e))
