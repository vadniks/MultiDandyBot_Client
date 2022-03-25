import tkinter as tk
from launcher import Launcher


WIDTH = 1000
HEIGHT = 600


class App(tk.Frame):

    def __init__(S, master):
        super(App, S).__init__(master)

        S.pack()

        Launcher(S)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Client')
    root.geometry(f'{WIDTH}x{HEIGHT}')

    app = App(root)
    app.mainloop()
