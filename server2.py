import socket,time
from PIL import Image, ImageGrab
import io
import pyautogui
import datetime


current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

file_name = f"log {current_time}.txt"

'''with open(file_name, 'a') as file:
    file.write(f"[{datetime.datetime.now().strftime("%H : %M : %S")} INFO] file running\n")'''


def serve():

    addr='172.16.11.13'
    port=10000
    '''with open(file_name, 'a') as file:
        file.write(f"[{datetime.datetime.now().strftime("%H : %M : %S")} INFO] socket server running on {addr}:{port}\n")'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (addr, port)
    sock.bind(server_address)

    # 监听传入连接
    sock.listen(1)

    try:
        '''with open(file_name, 'a') as file:
            file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} INFO] waiting for connection\n")'''
        connection, client_address = sock.accept()
        '''with open(file_name, 'a') as file:
            file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} INFO] connection from {client_address}\n")'''
        recfps=connection.recv(4)
        fps=int.from_bytes(recfps,byteorder='big', signed=True)
        '''with open(file_name, 'a') as file:
            file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} INFO] fps set to {fps}\n")'''
        try:
            while True:
                
                screenshot = ImageGrab.grab()
            
                img_byte_arr = io.BytesIO()
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
                    pyautogui.moveTo(mousex, mousey)
                    pyautogui.click()
                    '''with open(file_name, 'a') as file:
                        file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} INFO] left clicking at {mousex},{mousey}\n")
'''
                elif (mouseupdate==b'2'):

                    recmousex=connection.recv(4)
                    recmousey=connection.recv(4)
                    mousex=int.from_bytes(recmousex, byteorder='big', signed=True)
                    mousey=int.from_bytes(recmousey, byteorder='big', signed=True)
                    pyautogui.moveTo(mousex, mousey)
                    pyautogui.rightClick()
                    '''with open(file_name, 'a') as file:
                        file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} INFO] right clicking at {mousex},{mousey}\n")'''
 
                elif(mouseupdate==b'0'):
                    pass
                else :
                    '''with open(file_name, 'a') as file:
                        file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} Warning] unsupported mouse operation from client :{mouseupdate}\n")'''

                time.sleep(int(fps*1.0/1000))

                '''# 接收数据
                data = connection.recv(1024)
                print(f'收到数据: {data.decode()}')

                # 发送响应
                response = '这是服务器的响应'
                connection.sendall(response.encode())
        '''
        except Exception as e:
            '''with open(file_name, 'a') as file:
                file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} WARNING] {repr(e)}\n")'''
        finally:
            '''with open(file_name, 'a') as file:
                file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} INFO] closing connection {client_address}\n")
            connection.close()'''
    except Exception as e:
        '''with open(file_name, 'a') as file:
            file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} WARNING] {repr(e)}\n")'''
    finally:
        '''with open(file_name, 'a') as file:
            file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} INFO] closing socket\n")'''
        sock.close()
while True:
    try:
        serve()
    except Exception as e:
        '''with open(file_name, 'a') as file:
            file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")} WARNING] {repr(e)}\n")
'''