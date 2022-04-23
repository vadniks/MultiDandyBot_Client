from tkinter import Tk, Frame
import launcher as lc
import sync as sc
from core import game

WIDTH = 600
HEIGHT = 300
SCRIPT_STUB = 'def script(check, x, y): pass'

# noinspection PyMethodParameters
class App(Frame):

    def __init__(S, root):
        super(App, S).__init__(root)
        S.pack()
        lc.init(S, root)


if __name__ == '__main__':
    root = Tk()
    root.title('Client')
    root.geometry(f'{WIDTH}x{HEIGHT}')

    game.bindKeys(root)

    app = App(root)
    app.mainloop()

    sc.quitt()
