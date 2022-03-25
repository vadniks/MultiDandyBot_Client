import tkinter as tk
from tkinter import messagebox as msg

from main import IApp
from sync import Sync


# noinspection PyMethodParameters
class Launcher:
    nameEn: tk.Entry
    scriptBx: tk.Text
    app: IApp

    def __init__(S, frame: tk.Frame, app: IApp):
        S.app = app

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
        name = S.nameEn.get()
        script = S.scriptBx.get('1.0', 'end-1c')

        if len(name) == 0 or len(script) == 0:
            msg.showerror('Error', 'Text fields are empty')
            return

        sid = Sync.newSession(name, script)
        if sid is None:
            msg.showerror('Error', 'Unable to retrieve session')
            exit(1)

        S.app.setSessionId(sid)
