from tkinter import Frame, Label, Entry, Text, Button
from enum import Enum
from tkinter import messagebox as msg
import sync as sc


class State(Enum):
    LAUNCH = 0
    LOBBY = 1


mainLb: Label

state: State = State.LAUNCH


def init(frame: Frame):
    global mainLb

    mainLb = Label(frame, text='Welcome', font=("TkDefaultFont", 16))

    loginBt = Button(frame, text='Login', width=30)
    loginBt.configure(command=lambda: onLoginBt(nameEn, scriptBx, loginBt))

    nameEn = Entry(frame)
    scriptBx = Text(frame)

    mainLb.pack()
    loginBt.pack()
    nameEn.pack()
    scriptBx.pack()


def onLoginBt(nameEn: Entry, scriptBx: Text, loginBt: Button):
    name = nameEn.get()
    script = scriptBx.get('1.0', 'end-1c')

    if len(name) == 0 or len(script) == 0:
        msg.showerror('Error', 'Text fields are empty')
        return

    if not sc.newSession(name, script):
        msg.showerror('Error', 'Unable to retrieve session')
    else:
        lobby(nameEn, scriptBx, loginBt)


def lobby(nameEn: Entry, scriptBx: Text, loginBt: Button):
    global mainLb, state
    state = State.LOBBY

    mainLb.configure(text='Lobby')
    mainLb.pack()

    nameEn.pack_forget()
    scriptBx.pack_forget()
    loginBt.pack_forget()
