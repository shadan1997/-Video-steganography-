# note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
# install stegano, python-opencv, python3-tk, ffmpeg
import tkinter
import os
import shutil
import math
import base64
import cv2
import ed

from stegano import lsb
from tkinter.ttk import Progressbar
from subprocess import call, STDOUT
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from PIL import Image

video_path = ''
img_path = ''

print("video steganography")
root = tkinter.Tk()
root.title("Video_Steganography")
root.configure(bg="dark slate gray")


def split_string(s_str, count=10):
    per_c = math.ceil(len(s_str) / count)
    c_cout = 0
    out_str = ''
    split_list = []
    for s in s_str:
        out_str += s
        c_cout += 1
        if c_cout == per_c:
            split_list.append(out_str)
            out_str = ''
            c_cout = 0
    if c_cout != 0:
        split_list.append(out_str)
    return split_list


def frame_extraction(video):
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
    temp_folder = "./tmp"
    print("[INFO] tmp directory is created")
    video_cap = cv2.VideoCapture(video)
    count = 0
    while True:
        success, image = video_cap.read()
        if not success:
            print("[ERR] Some error occurred", success)
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1


# for type= text:10 img:500
def encode_string(input_string, types=10, temp="./tmp/"):
    split_string_list = split_string(input_string, types)
    for i in range(0, len(split_string_list)):
        f_name = "{}{}.png".format(temp, i)
        secret_enc = lsb.hide(f_name, split_string_list[i])
        secret_enc.save(f_name)
        print("[INFO] frame {} holds {}".format(f_name, split_string_list[i]))


def decode_string(video):
    progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
    progress.grid(row=9, column=0, columnspan=3, padx=10, pady=10)
    frame_extraction(video)
    secret = []
    tmp = "./tmp/"
    progress['value'] = 20
    root.update_idletasks()
    for i in range(len(os.listdir(tmp))):
        f_name = "{}{}.png".format(tmp, i)
        # print("[INFO] Decoding frame {}", f_name)
        secret_dec = lsb.reveal(f_name)
        # print("[INFO] Got {} from frame {}", secret_dec, f_name)
        if secret_dec is None:
            break
        secret.append(secret_dec)

    print(''.join([i for i in secret]))
    e2.delete(0, "end")
    e2.insert(0, ''.join([i for i in secret]))
    progress['value'] = 100
    root.update_idletasks()
    clean_tmp()
    progress.destroy()


def clean_tmp(path="./tmp"):
    if os.path.exists(path):
        shutil.rmtree(path)
        print("[INFO] tmp files are cleaned up")


# select a carrier video file
def open_file():
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    file = askopenfile(initialdir=desktop, mode='r', filetypes=[('Video Files', '*.mp4'), ('Video Files', '*.mov')])
    if file is None:
        print("No file selected")
        messagebox.showwarning("warning", "Select a video file")
    else:
        print("file name:", file.name)
        e1.delete(0, "end")
        e1.insert(0, file.name)
        print(os.path.basename(file.name))
        global video_path
        video_path = os.path.basename(file.name)
        print('[info]', video_path)
        shutil.copy(file.name, os.getcwd())


# select an stego_image file from desktop
def open_file_for_image():
    print("openfile")
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    file = askopenfile(initialdir=desktop, mode='r',
                       filetypes=[('Img', '*.png'), ('Img', '*.jpg'), ('Img', '*.bmp'), ('Img', '*.jpeg')])
    if file is None:
        print("No file selected")
        messagebox.showwarning("warning", "Select an image file")
    else:
        print("file name:", file.name)
        e3.delete(0, "end")
        e3.insert(0, file.name)
        print(os.path.basename(file.name))
        global img_path
        img_path = os.path.basename(file.name)
        print('[info]', img_path)
        shutil.copy(file.name, os.getcwd())


def tmp_show_image():
    Image.open("text.png").show()


# encoding image into video where image in img_path and video in video_path
def encode_image_into_video():
    if e4.get() != '':
        key = e4.get()
    else:
        key = 'python'
    print("[info] key", key)
    ed.pixelchange(img_path)
    ed.encryption_with_aes(img_path, ed.SALT, img_path, key)
    progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
    progress.grid(row=9, column=1, columnspan=4)
    print("|Encrypt| img in video start")
    print("image: ", img_path)
    print("video:", video_path)
    progress['value'] = 10
    root.update_idletasks()
    with open(img_path, "rb") as image:
        bstr = base64.b64encode(image.read())
    print(bstr)
    f_name = video_path
    input_string = str(bstr)
    progress['value'] = 20
    root.update_idletasks()
    frame_extraction(f_name)
    progress['value'] = 40
    root.update_idletasks()
    call(["ffmpeg", "-i", f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"], stdout=open(os.devnull, "w"),
         stderr=STDOUT)
    encode_string(input_string, 500)
    call(["ffmpeg", "-i", "tmp/%d.png", "-vcodec", "png", "tmp/video.mov", "-y"], stdout=open(os.devnull, "w"),
         stderr=STDOUT)
    progress['value'] = 60
    root.update_idletasks()
    call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mp4", "-y"],
         stdout=open(os.devnull, "w"), stderr=STDOUT)
    progress['value'] = 80
    root.update_idletasks()
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    progress['value'] = 90
    root.update_idletasks()
    shutil.copy("video.mp4", desktop)
    print("|Info| encryption image in video is Done....")
    progress['value'] = 100
    root.update_idletasks()
    clean_tmp()
    progress.destroy()


# decoding image from video where video is in video_path
def decode_image_form_video():
    # video.mp4
    progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
    progress.grid(row=9, column=1, columnspan=4)
    print("video_decoding start")
    progress['value'] = 20
    root.update_idletasks()
    frame_extraction(video_path)
    secret = []
    tmp = "./tmp/"
    progress['value'] = 40
    root.update_idletasks()
    for i in range(len(os.listdir(tmp))):
        f_name = "{}{}.png".format(tmp, i)
        # print("[INFO] Decoding frame {}", f_name)
        secret_dec = lsb.reveal(f_name)
        # print("[INFO] Got {} from frame {}", secret_dec, f_name)
        if secret_dec is None:
            break
        secret.append(secret_dec)
    video_data = ''.join([i for i in secret]) #making paragraph of list item
    progress['value'] = 80
    root.update_idletasks()
    clean_tmp()
    print("video_decoding start done")
    string_to_rgb(video_data)
    progress.destroy()


def string_to_rgb(bstr):
    print("stringToRGB")
    b_bstr = bstr[2:]
    #b_bstr = bstr
    x = base64.b64decode(b_bstr)
    fin = open("sample.enc", "wb") #recive file
    fin.write(x)
    fin.close()
    #converting decryption resuffle
    if e4.get() != '':
        key = e4.get()
    else:
        key = 'python'
    print("[info] key", key)
    ed.decryption_with_aes("sample.enc",ed.SALT,"sample.png",key)
    ed.pixelchange("sample.png")
    print("image file save as sample.png")
    global img_path
    img_path = "sample.png"
    Image.open("sample.png").show()
    print("stringToRGB done")
    copy_to_desktop("sample.png")


# play button
def play_btn():
    if video_path == '':
        print("file not found")
    else:
        print("file is:", video_path)
        play_video(video_path)


def copy_to_desktop(file_name):
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    shutil.copy(file_name, desktop)


# play a video using vlc
def play_video(video_name):
    try:
        print("|cmd| 'vlc' ", video_name)
        x = os.system('vlc "%s"' % video_name)
        if x != 0:
            messagebox.showerror("Req:", "install vlc player")
    except:
        print("error:No media player found")


def encrypt_message():
    progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')
    progress.grid(row=9, column=1, columnspan=4)
    print("|Encrypt| method invoke")
    f_name = video_path

    input_string = e2.get()
    progress['value'] = 20
    root.update_idletasks()
    frame_extraction(f_name)
    progress['value'] = 30
    root.update_idletasks()
    call(["ffmpeg", "-i", f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"], stdout=open(os.devnull, "w"),
         stderr=STDOUT),
    progress['value'] = 40
    root.update_idletasks()
    encode_string(input_string)
    progress['value'] = 50
    root.update_idletasks()
    call(["ffmpeg", "-i", "tmp/%d.png", "-vcodec", "png", "tmp/video.mov", "-y"], stdout=open(os.devnull, "w"),
         stderr=STDOUT)
    progress['value'] = 60
    root.update_idletasks()
    call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mp4", "-y"],
         stdout=open(os.devnull, "w"), stderr=STDOUT)
    progress['value'] = 70
    root.update_idletasks()
    # desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # shutil.copy("video.mp4", desktop)
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    progress['value'] = 80
    root.update_idletasks()
    shutil.copy("video.mp4", desktop)
    print("|Info| Done....")
    progress['value'] = 100
    root.update_idletasks()
    clean_tmp()
    progress.destroy()


def decrypt_message():
    decode_string(video_path)


def clean_ui():
    print('[info] cleaning ui:')
    e1.delete('0', "end")
    e2.delete('0', "end")
    e3.delete('0', "end")
    e4.delete('0', "end")
    c_box.set('select')
    global video_path
    video_path = ''
    global img_path
    img_path = ''


def go_button():
    print("go_button invoke")
    print('[info] checkbox1', c_box.get())
    print('[info] video name:', video_path)
    print('[info] msg:', e2.get())
    print('[info] image name:', img_path)
    if e1.get() == '':
        messagebox.showerror("Error", "Video is not selected")
    if c_box.get() == 'Encrypt_Message':
        if e2.get() == '':
            messagebox.showwarning("Warning", "put some message in message box.")
        else:
            encrypt_message()
    elif c_box.get() == 'Decrypt_Message':
        decrypt_message()
    elif c_box.get() == 'Encrypt_Image':
        if e3.get() == '':
            messagebox.showwarning("Warning", "select an image first.")
        else:
            encode_image_into_video()
    elif c_box.get() == 'Decrypt_Image':
        decode_image_form_video()
    else:
        print("select an operation")
        messagebox.showwarning("Warning", "select an operation first")


def show_image():
    print("show image invoke:")
    if img_path == '':
        print("file not found")
    else:
        Image.open(img_path).show()


# creating entries and positioning them on the grid
e1 = Entry(root)
e1.grid(row=10, column=2)
e2 = Entry(root)
e2.grid(row=11, column=2)
e3 = Entry(root)
e3.grid(row=14, column=2)
e4 = Entry(root)  #for key Default:python
e4.insert(0,'python')
e4.grid(row=13, column=2)
# creating labels and positioning them on the grid
label_1 = Label(root, bg="dark slate gray", fg="white", text='Video path')
label_1.grid(row=10, column=1)
label_2 = Label(root, bg="dark slate gray", fg="white", text='Plain text')
label_2.grid(row=11, column=1)
label_2 = Label(root, bg="dark slate gray", fg="white", text='Key')
label_2.grid(row=13, column=1)
label_3 = Label(root, bg="dark slate gray", fg="white", text="Operation :").grid(column=1, row=12, padx=10, pady=10)
label_4 = Label(root, bg="dark slate gray", fg="white", text="Image path").grid(column=1, row=14, padx=10, pady=10)

# creating checkbox and positioning them on the grid
c_box = ttk.Combobox(root)
c_box['values'] = ('Encrypt_Message', 'Decrypt_Message', 'Encrypt_Image', 'Decrypt_Image')
c_box.grid(row=12, column=2, )
c_box.set('select')

# creating Buttons and positioning them on the grid
b1 = Button(root, text='Browse', bg="teal", fg="white", command=lambda: open_file())
b1.grid(row=10, column=3, padx=10, pady=10)
b2 = Button(root, text="play video", bg="teal", fg="white", command=play_btn)
b2.grid(row=13, column=3, padx=10, pady=10)
b3 = Button(root, text="load", bg="teal", fg="white", command=open_file_for_image)
b3.grid(row=14, column=3, padx=10, pady=10)
b4 = Button(root, text="Go", bg="teal", fg="white", command=go_button)
b4.grid(row=15, column=3, padx=10, pady=10)
b3 = Button(root, text="clear", bg="teal", fg="white", command=clean_ui)
b3.grid(row=15, column=1, padx=10, pady=10)
b5 = Button(root, text="View Image", bg="teal", fg="white", command=show_image)
b5.grid(row=15, column=2, padx=10, pady=10)

root.mainloop()
