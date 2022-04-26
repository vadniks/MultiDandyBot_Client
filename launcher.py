from tkinter import Frame, Label, Entry, Text, Button, Tk, Listbox, END
from enum import Enum
from tkinter import messagebox as msg
from typing import List, Callable, Tuple
import sync as sc
import core.game as cr
from main import SCRIPT_STUB


class _State(Enum):
    LAUNCH = 0
    LOBBY = 1


_frame: Frame
_root: Tk
_mainLb: Label
_subtxLb: Label
_soloBt: Button
_playersLsb: Listbox
_readyBt: Button

_state: _State = _State.LAUNCH
_players: List[Tuple[int, str]]


def init(__frame: Frame, __root: Tk):
    global _frame, _mainLb, _root
    _frame = __frame
    _root = __root

    _mainLb = Label(_frame, text='Welcome', font=("TkDefaultFont", 16))

    loginBt = Button(_frame, text='Login', width=30)
    loginBt.configure(command=lambda: onLoginBt(nameEn, scriptBx, loginBt))

    nameEn = Entry(_frame)
    scriptBx = Text(_frame)
    scriptBx.insert('1.0', SCRIPT_STUB)

    _mainLb.pack()
    loginBt.pack()
    nameEn.pack()
    scriptBx.pack()


def onLoginBt(nameEn: Entry, scriptBx: Text, loginBt: Button):
    name = nameEn.get()
    _root.title('Client : ' + name)
    script = scriptBx.get('1.0', 'end-1c')

    if len(name) == 0 or len(script) == 0:
        msg.showerror('Error', 'Text fields are empty')
        return

    if sc.connect(name, script):
        lobby(nameEn, scriptBx, loginBt)
    else:
        msg.showerror(message='Connection failed or name already exists')


def lobby(nameEn: Entry, scriptBx: Text, loginBt: Button):
    global _mainLb, _state, _frame, _subtxLb, _soloBt, _readyBt
    _state = _State.LOBBY

    _mainLb.configure(text='Lobby')
    _mainLb.pack()

    nameEn.pack_forget()
    scriptBx.pack_forget()
    loginBt.pack_forget()

    _subtxLb = Label(_frame, font=("TkDefaultFont", 10), text='Waiting for players...')
    _subtxLb.pack()

    loadLeaderBoard()

    def script(): return scriptBx.get('1.0', 'end')

    _readyBt = Button(_frame, text='Mark ready', width=30,
        command=lambda: sc.notifyPlayerIsReady())
    _readyBt.pack()

    _soloBt = Button(_frame, text='Play solo', width=30,
        command=lambda: startGame(script, True))
    _soloBt.pack()

    sc.waitForPlayers(lambda players: onWait(players, _subtxLb), lambda: startGame(script, False))


def loadLeaderBoard():
    global _playersLsb
    _playersLsb = Listbox(_frame)

    #                  name score
    players: List[Tuple[str, int]] = sc.getSavedPlayers()
    [_playersLsb.insert(END, f'{i[0]} got {i[1]} gold') for i in players]
    _playersLsb.pack()


dx = 0


def clearFrame():
    global _mainLb, _subtxLb, _soloBt, _playersLsb
    _mainLb.pack_forget()
    _subtxLb.pack_forget()
    _readyBt.pack_forget()
    _soloBt.pack_forget()
    _playersLsb.pack_forget()


#                               id  name status
def onWait(players: List[Tuple[int, str, bool]], subtxLb: Label):
    global dx, _players
    _players = players

    tx = subtxLb['text']
    subtxLb['text'] = tx[:-1] + {0: '|', 1: '/', 2: '-', 3: '\\'}[dx]
    dx = 0 if dx == 3 else dx + 1


def startGame(scriptGetter: Callable, solo: bool):
    sc.solo = len(_players) == 0 or solo
    _players.insert(0, (sc.pid, sc.name))

    clearFrame()
    cr.start_game(_frame, _players, lambda w, h: _root.geometry(f'{w}x{h}'), scriptGetter(), _root)
