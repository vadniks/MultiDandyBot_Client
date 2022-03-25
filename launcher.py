import tkinter as tk
from tkinter import messagebox as msg


class Launcher:
    nameEn: tk.Entry
    scriptBx: tk.Text

    # noinspection PyMethodParameters
    def __init__(S, frame: tk.Frame):
        mainLb = tk.Label(frame, text='Welcome', font=("TkDefaultFont", 16))

        loginBt = tk.Button(frame, text='Login', width=30)
        loginBt.configure(command=S.onLoginBt)

        S.nameEn = tk.Entry(frame)
        S.scriptBx = tk.Text(frame)

        mainLb.pack()
        loginBt.pack()
        S.nameEn.pack()
        S.scriptBx.pack()

    def onLoginBt(S):
        print(len(S.nameEn.get()))
        print(len(S.scriptBx.get('1.0', 'end-1c')))
        if len(S.nameEn.get()) == 0 or len(S.scriptBx.get('1.0', 'end-1c')) == 0:
            msg.showerror('Error', 'Text fields are empty')
