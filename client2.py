import socket
import tkinter as tk
from PIL import Image, ImageTk
import io

fps=40

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mouseposx=0
mouseposy=0
mouseupdate=False
mouseop="none"
cwidth=480
# 连接到服务器
server_address = ('172.16.11.13', 10000)
sock.connect(server_address)

sock.sendall(fps.to_bytes(4,byteorder='big'))
def update_image():
    
    global fps,sock
    mode = sock.recv(1)
    if (mode==b'1'):
        # 接收图像数据长度
        data_length = sock.recv(4)
        if not data_length:
            return
        
        # 接收图像数据
        img_byte_arr = b''
        while len(img_byte_arr) < int.from_bytes(data_length, byteorder='big'):
            packet = sock.recv(4096)
            if not packet:
                break
            img_byte_arr += packet
        
        # 将字节流转换为图像
        img = Image.open(io.BytesIO(img_byte_arr))
        global cwidth
        img = img.resize((int(cwidth), int(int(cwidth)*1080/1920.0)))
        photo = ImageTk.PhotoImage(image=img)
        label.config(image=photo)
        label.image = photo
        

        flag=True
        #发送鼠标位置
        #先判断功能是否开启
        print("即将判断功能是否开启")
        if(flag==True):
            print("功能已开启，确认是否有更新")
            global mouseposy,mouseposx,mouseupdate,mouseop
            if (mouseupdate):
                print("即将发送")
                if (mouseop=="left"):
                    print("进行了一次左键单击")
                    sock.sendall(b'1')
                    sock.sendall(mouseposx.to_bytes(4, byteorder='big'))
                    sock.sendall(mouseposy.to_bytes(4, byteorder='big'))
                    mouseupdate=False
                if (mouseop=="right"):
                    print("进行了一次右键单击")
                    sock.sendall(b'2')
                    sock.sendall(mouseposx.to_bytes(4, byteorder='big'))
                    sock.sendall(mouseposy.to_bytes(4, byteorder='big'))
                    mouseupdate=False
            else:
                print("没有鼠标操作")
                sock.sendall(b'0')
        else:
            print("已关闭功能")
            sock.sendall(b'0')
        root.after(fps, update_image)

    
    else :
        print("不支持的功能：",mode)
try:
    def get_window_position_and_size(window):
        position_and_size = window.geometry()
        width_height = position_and_size.split('+')[0]
        width = int(width_height.split('x')[0])
        height = int(width_height.split('x')[1])
        return (width, height)

    def on_click_left(event):
        width, height = get_window_position_and_size(root)
        print(f"Mouse left clicked at: ({int((int(event.x))*(1920/float(width)))}, {int((int(event.y))*(1080/float(height)))})")
        global mouseposx,mouseposy,mouseupdate,mouseop
        mouseposx=int((int(event.x))*(1920/float(width)))
        mouseposy=int((int(event.y))*(1080/float(height)))
        print("更新了鼠标左单击")
        mouseupdate=True
        mouseop="left"

    def on_click_right(event):
        width, height = get_window_position_and_size(root)
        print(f"Mouse left clicked at: ({int((int(event.x))*(1920/float(width)))}, {int((int(event.y))*(1080/float(height)))})")
        global mouseposx,mouseposy,mouseupdate,mouseop
        mouseposx=int((int(event.x))*(1920/float(width)))
        mouseposy=int((int(event.y))*(1080/float(height)))
        print("更新了鼠标右单击")
        mouseupdate=True
        mouseop="right"

    def update_screen_size_label(value):
        global cwidth
        cwidth=int(value)
        label2.config(text="屏幕大小： " + value)
    def update_fps_label(value):
        global setfps
        setfps=int(1000*1.0/int(value))
        label2.config(text="帧率： " + value)
    root = tk.Tk()
    root.title("屏幕")


    label = tk.Label(root)
    label.pack()
    root.bind("<Button-1>", on_click_left)
    root.bind("<Button-3>", on_click_right)

    update_image()


    
    settings = tk.Tk()
    settings.title("settings")


    label2 = tk.Label(settings, text="屏幕大小： 1")
    label2.pack()


    scale = tk.Scale(settings, from_=1, to=1920, orient=tk.HORIZONTAL, length=300,
                 troughcolor='lightgray', sliderlength=20, sliderrelief='solid',
                 bg='white', highlightthickness=20, command=update_screen_size_label)
    scale.pack()
    

    root.mainloop()
    settings.mainloop()
finally:
    sock.close()
    