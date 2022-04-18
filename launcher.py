import tkinter
from tkinter import Frame, Label, Entry, Text, Button, Tk
from enum import Enum
from tkinter import messagebox as msg
import sync as sc
import core.main as cr


class State(Enum):
    LAUNCH = 0
    LOBBY = 1


frame: Frame
root: Tk
mainLb: Label

state: State = State.LAUNCH


def init(_frame: Frame, _root: Tk):
    global frame, mainLb, root
    frame = _frame
    root = _root

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
    global mainLb, state, frame
    state = State.LOBBY

    mainLb.configure(text='Lobby')
    mainLb.pack()

    nameEn.pack_forget()
    scriptBx.pack_forget()
    loginBt.pack_forget()

    subtxLb = Label(frame, font=("TkDefaultFont", 10), text='Waiting for players...')
    subtxLb.pack()

    def script(): return scriptBx.get('1.0', 'end')

    soloBt = Button(frame, text='Play solo', width=30, command=lambda: startGame(True, script()))
    soloBt.pack()

    sc.waitForPlayers(lambda: startGame(False, scriptBx.get('1.0', 'end')), lambda: onWait(subtxLb))


dx = 0


def onWait(subtxLb: Label):
    global dx
    tx = subtxLb['text']
    subtxLb['text'] = tx[:-1] + {0: '|', 1: '/', 2: '-', 3: '\\'}[dx]
    dx = 0 if dx == 3 else dx + 1


def startGame(solo: bool, script: str):

    cr.start_game(frame, lambda w, h: root.geometry(f'{w}x{h}'))
