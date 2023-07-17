import os
import shutil
from tkinter import ttk
from stegano import lsb
from tkinter import *
from tkinter import messagebox
from PIL import Image
# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile
image_path = ''


def open_file():
    print("openfile")
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    file = askopenfile(initialdir=desktop, mode='r',
                       filetypes=[('Img', '*.png'), ('Img', '*.jpg'), ('Img', '*.bmp'), ('Img', '*.jpeg')])
    if file is None:
        print("No file selected")
        messagebox.showwarning("warning", "Select an image file")
    else:
        print("file name:", file.name)
        e1.delete(0, "end")
        e1.insert(0, file.name)
        print(os.path.basename(file.name))
        global image_path
        image_path = os.path.basename(file.name)
        print('[info]', image_path)
        shutil.copy(file.name, os.getcwd())


def open_img():
    print("open image")
    if image_path != '':
        image(image_path)
    else:
        messagebox.showwarning("warning", "select an image")


def encrypt():
    print("encrypt")
    msg = e2.get()
    print("|Msg|", msg)
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    secret = lsb.hide(image_path, msg)
    secret.save('encoded_image.png')
    shutil.copy('encoded_image.png', desktop)
    print("encryption done")


def decrypt():
    print("decrypt")
    msg = lsb.reveal(image_path)
    print("|Msg|", msg)
    e2.delete(0, "end")
    e2.insert(0, msg)
    print("decryption done")


def image(file_name):
    return Image.open(file_name).show()


def submit():
    print("submit")
    if c_box.get() == 'encryptMessage':
        if e2.get() == '':
            messagebox.showwarning("Warning", "put some msg in msg box.")
        else:
            encrypt()
    elif c_box.get() == 'decryptMessage':
        decrypt()
    else:
        print("select an operation")
        messagebox.showwarning("Warning", "select an operation first")


def clean_ui():
    print('[info] cleaning ui:')
    e1.delete('0', "end")
    e2.delete('0', "end")
    c_box.set('select')
    global image_path
    image_path = ''


print("iw")
root = Tk(className='image steganography')
root['background'] = 'dark slate gray'
# creating labels and positioning them on the grid
label1 = Label(root, text='File Path', fg="white", bg='dark slate gray')
label1.grid(row=10, column=1)
label2 = Label(root, text='Plain Text', fg="white", bg='dark slate gray')
label2.grid(row=11, column=1)

# creating entries and positioning them on the grid
e1 = Entry(root)
e1.grid(row=10, column=2)
e2 = Entry(root)
e2.grid(row=11, column=2)

btn = Button(root, bg='teal', text='Browse', fg="white", command=lambda: open_file())
btn.grid(row=10, column=3, padx=10, pady=10)

label3 = Label(root, fg="white", text="Operation :", bg='dark slate gray')
label3.grid(column=1,   row=12, padx=10, pady=25)

c_box = ttk.Combobox(root)
c_box['values'] = ('encryptMessage', 'decryptMessage')
c_box.grid(column=2, row=12)
c_box.set('select')
b2 = Button(root, text="Submit", bg="teal", fg="white", command=submit)
b2.grid(row=13, column=3, padx=10, pady=10)

b3 = Button(root, text="clear", bg="teal", fg="white", command=clean_ui)
b3.grid(row=13, column=1,  padx=10, pady=10)

b4 = Button(root, text="Image", bg="teal", fg="white", command=open_img)
b4.grid(row=13, column=2,  padx=10, pady=10)

root.mainloop()
