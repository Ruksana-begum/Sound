from tkinter import *
from tkinter import messagebox as mb
from PIL import Image
import wave

root = Tk()
root.title("Audio Steganography - Hiding a secret message in audio")
root.geometry("300x250")
root.resizable(False, False)
root.configure(bg = "#2f4155")
def ceaser_encrypt(plain_text,key):
    encrypted = ""
    for c in plain_text:
        if c.isupper(): #check if it's an uppercase character
            c_index = ord(c) - ord('A')
            # shift the current character by key positions
            c_shifted = (c_index + key) % 26 + ord('A')
            c_new = chr(c_shifted)
            encrypted += c_new
        elif c.islower(): #check if its a lowecase character
            # subtract the unicode of 'a' to get index in [0-25) range
            c_index = ord(c) - ord('a')
            c_shifted = (c_index + key) % 26 + ord('a')
            c_new = chr(c_shifted)
            encrypted += c_new
        elif c.isdigit():
            # if it's a number,shift its actual value
            c_new = (int(c) + key) % 10
            encrypted += str(c_new)
        else:
            # if its neither alphabetical nor a number, just leave it like that
            encrypted += c
       
    return encrypted
def main_encryption(aud,text,key,new_aud):
    if(aud == '' or text == '' or key == '' or new_aud == ''  ):
        mb.showwarning("showwarning", "Enter every field")
        exit()
    #read wave audio file
    song = wave.open(aud, mode='rb')
    #read frames and convert to byte array
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    s= text
    k = int(key)
    #encrypting
    string = ceaser_encrypt(s,k)
    #completed encryption
    string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
    #Convert text to bit array
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
    #replace LSB of each byte of the audio data by one bit from text bit array
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    #getting the modified bytes
    frame_modified = bytes(frame_bytes)
    new_aud += '.wav'
    #writing bytes to new audio file
    with wave.open(new_aud, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)
    song.close()
def ceaser_decrypt(ciphertext, key):
    decrypted = ""
    for c in ciphertext:
        if c.isupper():
            c_index = ord(c) - ord('A')
            # shift the current character to left by key positions to get its original position
            c_og_pos = (c_index - key) % 26 + ord('A')
            c_og = chr(c_og_pos)
            decrypted += c_og

        elif c.islower():
            c_index = ord(c) - ord('a')
            c_og_pos = (c_index - key) % 26 + ord('a')
            c_og = chr(c_og_pos)
            decrypted += c_og

        elif c.isdigit():
            # if it's a number,shift its actual value
            c_og = (int(c) - key) % 10
            decrypted += str(c_og)

        else:
            # if its neither alphabetical nor a number, just leave it like that
            decrypted += c
   
    return decrypted
def main_decryption(aud1,key,strvar):
    if (aud1 == '' or key == ''):
        mb.showwarning("showwarning", "Enter every field")
        exit()
    song = wave.open(aud1, mode='rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    decoded = string.split("###")[0]
    k = int(key)
    #dec
    decMessage = ceaser_decrypt(decoded,k)
    #complted
    #print("Sucessfully decoded: "+decMessage)
    strvar.set(decMessage)
    song.close()

def encode_audio():
    encode_wn = Toplevel(root)
    encode_wn.title("Encode an Audio")
    encode_wn.geometry('600x300')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='AntiqueWhite')
    Label(encode_wn, text='Encode an Audio', font=("Comic Sans MS", 15), bg='AntiqueWhite').place(x=220, rely=0)
    Label(encode_wn, text='Enter the path to the Audio(with extension):', font=("Times New Roman", 13),bg='AntiqueWhite').place(x=10, y=50)
    Label(encode_wn, text='Enter the data to be encoded:', font=("Times New Roman", 13), bg='AntiqueWhite').place(x=10, y=90)
    Label(encode_wn, text='Enter the secret key:', font=("Times New Roman", 13), bg='AntiqueWhite').place(x=10, y=130)
    Label(encode_wn, text='Enter the output file name (without extension):', font=("Times New Roman", 13),bg='AntiqueWhite').place(x=10, y=170)
    aud_path = Entry(encode_wn, width=35)
    aud_path.place(x=350, y=50)
    text_to_be_encoded = Entry(encode_wn, width=35)
    text_to_be_encoded.place(x=350, y=90)
    secret_key = Entry(encode_wn, width = 35)
    secret_key.place(x=350,y=130)
    after_save_path = Entry(encode_wn, width=35)
    after_save_path.place(x=350, y=170)
    Button(encode_wn, text='Encode the Audio', font=('Helvetica', 12), bg='PaleTurquoise', command=lambda:
    main_encryption(aud_path.get(), text_to_be_encoded.get(), secret_key.get(),after_save_path.get())).place(x=220, y=250)

def decode_audio():
    decode_wn = Toplevel(root)
    decode_wn.title("Decode an Audio")
    decode_wn.geometry('600x400')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='Bisque')
    Label(decode_wn, text='Decode an Audio', font=("Comic Sans MS", 15), bg='Bisque').place(x=220, rely=0)
    Label(decode_wn, text='Enter the path to the audio (with extension):', font=("Times New Roman", 12),bg='Bisque').place(x=10, y=50)
    aud_entry = Entry(decode_wn, width=35)
    aud_entry.place(x=350, y=50)
    Label(decode_wn, text='Enter the secret key :', font=("Times New Roman", 12),bg='Bisque').place(x=10, y=90)
    sec_key = Entry(decode_wn, width = 35)
    sec_key.place(x=350,y=90)
    text_strvar = StringVar()
    Button(decode_wn, text='Decode the Audio', font=('Helvetica', 12), bg='PaleTurquoise', command=lambda:
           main_decryption(aud_entry.get(),sec_key.get(),text_strvar)).place(x=220, y=130)
    Label(decode_wn, text='Text that has been encoded in the audio:', font=("Times New Roman", 12), bg='Bisque').place(x=180, y=170)
    text_entry = Entry(decode_wn, width=94, text=text_strvar, state='disabled')
    text_entry.place(x=15, y=200, height=100)
#icon
image_icon = PhotoImage(file = "logo.jpg")
root.iconphoto(False, image_icon)

Label(root, text='Audio Steganography', font=('Comic Sans MS', 15), bg='NavajoWhite',wraplength=300).place(x=40, y=0)
Button(root, text='Encode', width=25, font=('Times New Roman', 13), bg='NavajoWhite', command=encode_audio).place(x=30, y=80)
Button(root, text='Decode', width=25, font=('Times New Roman', 13), bg='NavajoWhite', command=decode_audio).place(x=30, y=130)




root.mainloop()
