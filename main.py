from tkinter import Tk, Frame
import launcher as lc
import sync as sc
from core import game

WIDTH = 600
HEIGHT = 350
SCRIPT_STUB = 'def script(check, x, y): pass'
IS_DEBUG_ENABLED = True


# noinspection PyMethodParameters
class App(Frame):

    def __init__(S, _root):
        super(App, S).__init__(_root)
        S.pack()
        lc.init(S, _root)


if __name__ == '__main__':
    _root = Tk()
    _root.title('Client')
    _root.geometry(f'{WIDTH}x{HEIGHT}')

    game.bindKeys(_root)

    app = App(_root)
    app.mainloop()

    sc.saveCurrentPlayerResult()
    sc.quitt()
