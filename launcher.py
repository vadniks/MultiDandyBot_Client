import tkinter as tk
from tkinter import messagebox as msg
import sync as sc


nameEn: tk.Entry
scriptBx: tk.Text


def init(frame: tk.Frame):
    global nameEn, scriptBx

    mainLb = tk.Label(frame, text='Welcome', font=("TkDefaultFont", 16))

    loginBt = tk.Button(frame, text='Login', width=30)
    loginBt.configure(command=onLoginBt)

    nameEn = tk.Entry(frame)
    scriptBx = tk.Text(frame)

    mainLb.pack()
    loginBt.pack()
    nameEn.pack()
    scriptBx.pack()


def onLoginBt():
    global nameEn, scriptBx

    name = nameEn.get()
    script = scriptBx.get('1.0', 'end-1c')

    if len(name) == 0 or len(script) == 0:
        msg.showerror('Error', 'Text fields are empty')
        return

    if not sc.newSession(name, script):
        msg.showerror('Error', 'Unable to retrieve session')
        exit(1)
