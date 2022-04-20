from tkinter import Tk, Frame
import launcher as lc
import sync as sc


WIDTH = 1000
HEIGHT = 600


# noinspection PyMethodParameters
class App(Frame):

    def __init__(S, master):
        super(App, S).__init__(master)
        S.pack()
        lc.init(S, master)


if __name__ == '__main__':
    root = Tk()
    root.title('Client')
    root.geometry(f'{WIDTH}x{HEIGHT}')

    app = App(root)
    app.mainloop()

    sc.quitt()
