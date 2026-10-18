import tkinter as tk
from tkinter import filedialog    #文件选择模块

root = tk.Tk()   #创建主窗口对象
root.withdraw()  # 隐藏空白主窗口

filenames = filedialog.askopenfilenames(   #askopenfilenames() 打开文件选择对话框，返回选择的文件路径列表
    parent=root,                #绑定主窗口
    title='选择 STL 文件',
    filetypes=[('STL 文件', '*.stl')]           #设置文件类型筛选项
)

root.destroy()  # 释放 Tk 窗口
print(filenames)