from tkinter import Frame, Label, Entry, Text, Button, Tk
from enum import Enum
from tkinter import messagebox as msg
from typing import List, Callable, Tuple

import sync as sc
import core.gmain as cr
from main import SCRIPT_STUB


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
    scriptBx.insert('1.0', SCRIPT_STUB)

    mainLb.pack()
    loginBt.pack()
    nameEn.pack()
    scriptBx.pack()


def onLoginBt(nameEn: Entry, scriptBx: Text, loginBt: Button):
    name = nameEn.get()
    root.title('Client : ' + name)
    script = scriptBx.get('1.0', 'end-1c')

    if len(name) == 0 or len(script) == 0:
        msg.showerror('Error', 'Text fields are empty')
        return

    if not sc.newSession(name, script):
        msg.showerror('Error', 'Unable to retrieve session')
    else:
        lobby(nameEn, scriptBx, loginBt)


subtxLb: Label
soloBt: Button


def lobby(nameEn: Entry, scriptBx: Text, loginBt: Button):
    global mainLb, state, frame, subtxLb, soloBt
    state = State.LOBBY

    mainLb.configure(text='Lobby')
    mainLb.pack()

    nameEn.pack_forget()
    scriptBx.pack_forget()
    loginBt.pack_forget()

    subtxLb = Label(frame, font=("TkDefaultFont", 10), text='Waiting for players...')
    subtxLb.pack()

    def script(): return scriptBx.get('1.0', 'end')

    soloBt = Button(frame, text='Play solo', width=30, command=lambda: startGame([], script))
    soloBt.pack()

    sc.waitForPlayers(lambda players: startGame(players, script), lambda: onWait(subtxLb))


dx = 0


def clearFrame():
    global mainLb, subtxLb, soloBt
    mainLb.pack_forget()
    subtxLb.pack_forget()
    soloBt.pack_forget()


def onWait(subtxLb: Label):
    global dx
    tx = subtxLb['text']
    subtxLb['text'] = tx[:-1] + {0: '|', 1: '/', 2: '-', 3: '\\'}[dx]
    dx = 0 if dx == 3 else dx + 1


def startGame(players: List[Tuple[int, str]], scriptGetter: Callable):
    solo = len(players) == 0
    players.insert(0, (sc.pid, sc.name))

    clearFrame()
    cr.start_game(frame, players, lambda w, h: root.geometry(f'{w}x{h}'), scriptGetter())
