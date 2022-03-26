import tkinter as tk
import launcher as lc


WIDTH = 1000
HEIGHT = 600


# noinspection PyMethodParameters
class App(tk.Frame):

    def __init__(S, master):
        super(App, S).__init__(master)
        S.pack()
        lc.init(S)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Client')
    root.geometry(f'{WIDTH}x{HEIGHT}')

    app = App(root)
    app.mainloop()
