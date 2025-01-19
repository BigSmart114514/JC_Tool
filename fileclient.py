
from socket import SOCK_STREAM,AF_INET,socket
from json import loads
import tkinter as tk
from tkinter import ttk
ADDR='172.16.11.15'
PORT=10002
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
def get_files(path):
    sock = socket(AF_INET, SOCK_STREAM)
    server_address = (ADDR,PORT)
    print("connected to JC server")
    sock.connect(server_address)
    sock.sendall(len(path.encode("utf-8")).to_bytes(4, byteorder='big'))
    sock.sendall(path.encode("utf-8"))
    files=recv_sock(sock)
    if files:
        return loads(files)
    else:
        return []






path="C:\\"


def on_double_click(event):
    global path,tree,files
    item = tree.identify('item', event.x, event.y)
    item2=tree.set(item, "text")
    
    print(f"双击了: {item2}")
    if tree.set(item, "type")=="<dir>":
        path+=item2+"\\"
        #print(path)
        files=get_files(path)
        print(files)
        for i in tree.get_children():
            tree.delete(i)
        for file in files:
            tree.insert("", "end", values=(file[0],file[1]))
        
    else:
        if tree.set(item, 'text'):
            #os.system("start \"{}{}\"".format(path,tree.set(item, 'text')))
            pass
    #\"{tree.set(item, 'text')}\"
    # 在这里添加你的双击操作逻辑

def show_context_menu(event):
    global selected_item
    selected_item = tree.identify('item', event.x, event.y)  # 保存选中的行
    if selected_item:
        menu.post(event.x_root, event.y_root)

def menu_option1():
    print(f"执行菜单选项1，选中的行是: {selected_item}")
    # 在这里添加你的菜单选项1的逻辑

def menu_option2():
    print(f"执行菜单选项2，选中的行是: {selected_item}")
root = tk.Tk()
print("SB")
files=get_files(path)
print(len(files))


# 创建表格
tree = ttk.Treeview(root, columns=( "text","type"))
#tree.heading("#0", text="")
#tree.heading("icon", text="")
tree.heading("text", text="文本")
tree.heading("type", text="种类")




# 插入示例数据
for file in files:
    tree.insert("", "end", values=(file[0],file[1]))

scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

tree.bind("<Double-1>", on_double_click)
tree.bind("<Button-3>", show_context_menu)


menu = tk.Menu(root, tearoff=0)
menu.add_command(label="选项1", command=menu_option1)
menu.add_command(label="选项2", command=menu_option2)

tree.pack(fill='both', expand=True)
# 添加滚动条


# 添加输入框和前往按钮
entry = tk.Entry(root)
entry.pack()

def go_to():
    target = entry.get()
    try:
        item_id = tree.get_children()[int(target) - 1]
        tree.see(item_id)
        tree.selection_set(item_id)
    except (IndexError, ValueError):
        print("无效的行号")

go_button = tk.Button(root, text="前往", command=go_to)
go_button.pack()

# 添加返回按钮
def go_back():
    global path
    path=path.split("\\")
    path.pop()
    path.pop()
    print(path)
    path="\\".join(path)+"\\"
    files=get_files(path)
    for i in tree.get_children():
        tree.delete(i)
    for file in files:
        tree.insert("", "end", values=(file[0],file[1]))
back_button = tk.Button(root, text="返回", command=go_back)
back_button.pack()

root.mainloop()