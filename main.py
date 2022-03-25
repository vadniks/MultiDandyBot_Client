import tkinter as tk
from abc import ABC, abstractmethod

import launcher as lch


WIDTH = 1000
HEIGHT = 600


class IApp(ABC):
    @abstractmethod
    def setSessionId(S, sid: int): raise NotImplementedError


# noinspection PyMethodParameters
class App(tk.Frame, IApp):
    sessionId: int

    def __init__(S, master):
        super(App, S).__init__(master)
        S.pack()
        lch.Launcher(S, S)

    def setSessionId(S, sid: int):
        S.sessionId = sid


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Client')
    root.geometry(f'{WIDTH}x{HEIGHT}')

    app = App(root)
    app.mainloop()
