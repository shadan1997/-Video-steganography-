from Crypto.Cipher import AES
from Crypto import Random
import hashlib
from PIL import Image
import math

SALT = 'salt.enc'


def encryption_with_aes(fname, salt, oname, password):
    key = hashlib.md5(password.encode('UTF-8'))
    iv = Random.new().read(AES.block_size)
    iv_file = open(salt, "wb")
    # save Initial vector in iv.txt
    iv_file.write(iv)
    iv_file.close()
    input_file = open(fname, 'rb')
    # Reading image file
    input_data = input_file.read()
    input_file.close()
    cfb_cipher = AES.new(key.digest(), AES.MODE_CFB, iv)
    # encrypt
    enc_data = cfb_cipher.encrypt(input_data)
    enc_file = open(oname, 'wb')
    # doc save
    enc_file.write(enc_data)
    enc_file.close()


def decryption_with_aes(fname, salt, oname, password):
    key = hashlib.md5(password.encode('UTF-8'))
    enc_file2 = open(fname, 'rb')
    enc_data2 = enc_file2.read()
    enc_file2.close()
    iv_open = open(salt, 'rb')
    iv = iv_open.read()
    iv_open.close()
    cfb_decipher = AES.new(key.digest(), AES.MODE_CFB, iv)
    plain_data = cfb_decipher.decrypt(enc_data2)
    output_file = open(oname, "wb")
    output_file.write(plain_data)
    output_file.close()


def rot(arr, n, x1, y1):  # this is the function which rotates a given block
    temple = []
    for i in range(n):
        temple.append([])
        for j in range(n):
            temple[i].append(arr[x1+i, y1+j])
    for i in range(n):
        for j in range(n):
            arr[x1+i, y1+j] = temple[n-1-i][n-1-j]


def pixelchange(fname):
    im = Image.open(fname, "r")
    width, height = im.size
    arr = im.load()  # pixel data stored in this 2D array
    xres = width
    yres = height
    blocksize = 50  # blocksize
    for i in range(2, blocksize+1):
        for j in range(int(math.floor(float(xres)/float(i)))):
            for k in range(int(math.floor(float(yres)/float(i)))):
                rot(arr, i, j*i, k*i)
    for i in range(3, blocksize+1):
        for j in range(int(math.floor(float(xres)/float(blocksize+2-i)))):
            for k in range(int(math.floor(float(yres)/float(blocksize+2-i)))):
                rot(arr, blocksize+2-i, j*(blocksize+2-i), k*(blocksize+2-i))

    im.save(fname)
    print("Pixel CHANGE done!")

# pixelchange("test.jpg")
# input file name, iv, otput file name, password
# encryption_with_aes("test.jpg", "salt.enc", "encrypted.enc", 'hello')
# input file name, iv, otput file name, password
# decryption_with_aes("encrypted.enc", "salt.enc", "output.jpg", 'hello')
# pixelchange("test.jpg")
