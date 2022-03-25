import tkinter as tk
from abc import ABC, abstractmethod

from launcher import Launcher


WIDTH = 1000
HEIGHT = 600


class IApp(ABC):
    @abstractmethod
    def setSessionId(S, sid: int): pass


class App(tk.Frame, IApp):
    sessionId: int

    def __init__(S, master):
        super(App, S).__init__(master)
        S.pack()
        Launcher(S)

    def setSessionId(S, sid: int):
        S.sessionId = sid


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Client')
    root.geometry(f'{WIDTH}x{HEIGHT}')

    app = App(root)
    app.mainloop()
