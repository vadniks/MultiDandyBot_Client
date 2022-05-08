"""
MIT License

Copyright (c) 2022 Vad Nik (https://github.com/vadniks)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from tkinter import Tk, Frame
import launcher as lc
import sync as sc
from core import game

WIDTH = 600
HEIGHT = 350
SCRIPT_STUB = 'def script(check, x, y): pass'
IS_DEBUG_ENABLED = True
# TODO: debugging with "{ python main.py &; } && { python main.py &; } && { python main.py &; }"
# TODO: to start 3 separate instances of the client in the background


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
