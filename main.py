import os
from tkinter import *
from tkinter.ttk import *


def my_quit():
    print("quit")
    # gui.destroy()


def i_window():
    try:
        cmd = 'python3 iw.py'
        x = os.system(cmd)
        my_quit()
        raise x
    except:
        print("file not found: iw.py")


def v_window():
    try:
        cmd = 'python3 vw.py'
        x = os.system(cmd)
        my_quit()
        raise x
    except:
        print("file not found: vw.py")


gui = Tk(className='steganography')
# set window size
gui.geometry("400x300")
# set window color Icon_Steganography.png
gui['background'] = 'dark slate gray'
btn1 = Button(gui, text="Image", command=i_window)
btn1.place(x=100, y=140)
btn2 = Button(gui, text="Video", command=v_window)
btn2.place(x=200, y=140)

gui.mainloop()
