import tkinter as tk
from tkinter import ttk
import PIL.ImageTk
import PIL.Image
import os

def list_files(directory):
    try:
        files=[]
        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path):
                #print(f"{file} (文件)")
                files.append([file,f"{file.split('.')[-1]}文件"])
            elif os.path.isdir(full_path):
                #print(f"{file} (文件夹)")
                files.append([file,"<dir>"])

        return files
    except Exception as e:
        print(e)
        return [["拒绝访问","!error!"]]
path="C:\\"







def on_double_click(event):
    global path,tree,files
    item = tree.identify('item', event.x, event.y)
    item2=tree.set(item, "text")
    
    print(f"双击了: {item2}")
    if tree.set(item, "type")=="<dir>":
        path+=item2+"\\"
        #print(path)
        files=list_files(path)
        print(files)
        for i in tree.get_children():
            tree.delete(i)
        for file in files:
            tree.insert("", "end", values=(file[0],file[1]))
        
    else:
        if tree.set(item, 'text'):
            #print("start \"{}{}\"".format(path,tree.set(item, 'text')))
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
files=list_files(path)
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
    global path
    target = entry.get()
    print(target)
    try:
        
        files=list_files(target)
        for i in tree.get_children():
            tree.delete(i)
        for file in files:
            tree.insert("", "end", values=(file[0],file[1]))
        path=target.strip("\\")+"\\"
    except:
        print("SB")
go_button = tk.Button(root, text="前往", command=go_to)
go_button.pack()

# 添加返回按钮
def go_back():
    global path
    path=path.split("\\")
    if (len(path)!=2):
        
        path.pop()
        path.pop()
        print(path)
    path="\\".join(path)+"\\"
    files=list_files(path)
    print(path)
    
    for i in tree.get_children():
        tree.delete(i)
    for file in files:
        tree.insert("", "end", values=(file[0],file[1]))
back_button = tk.Button(root, text="返回", command=go_back)
back_button.pack()

root.mainloop()