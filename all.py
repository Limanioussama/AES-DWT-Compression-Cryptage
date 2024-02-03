from Crypto.Cipher import AES
from tkinter import *
import pywt
import cv2
import numpy as np
import os

# Define the input and output file paths
input_file = "4K_107.mp4"
compressed_file = "compressed_video.mp4"
decompressed_file = "decompressed_video.mp4"
# AES ENCRYPTION
key = b'Key of length 16'
iv = b'ivb of length 16'
#Path determination
cwd_original_1=os.getcwd()
cwd_original=os.path.join(cwd_original_1,"Encrypted")
cwd_original_decrypt=os.path.join(cwd_original_1,"Decrypted")




# Define the DWT compression function
def compress_frame(frame):
    # Perform DWT on the frame
    coeffs = pywt.dwt2(frame, 'haar')

    # Keep only the LL subband coefficients
    LL, (LH, HL, HH) = coeffs
    coeffs = LL, (np.zeros_like(LH), np.zeros_like(HL), np.zeros_like(HH))

    # Reconstruct the compressed frame
    compressed_frame = pywt.idwt2(coeffs, 'haar')

    # Convert the frame to unsigned 8-bit integers
    compressed_frame = np.uint8(compressed_frame)

    return compressed_frame

def compress_video():
    # Open the video file for reading
    cap = cv2.VideoCapture(input_file)

    # Get the video frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Get the video frame size
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a video writer object for the compressed video file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(compressed_file, fourcc, fps, (frame_width, frame_height), isColor=False)

    # Loop through the video frames
    while cap.isOpened():
        # Read the next frame
        ret, frame = cap.read()

        if ret == True:
            # Convert the frame to grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Compress the frame using DWT
            compressed_frame = compress_frame(frame)

            # Write the compressed frame to the video writer object
            out.write(compressed_frame)

        else:
            break

        # Release the video capture and writer objects
    cap.release()
    out.release()

def encrypt_video():
        try:
            os.mkdir(os.path.join(cwd_original_1,"Encrypted"))
        except:
            pass
        global key,iv,entry_for_folder,root
        file_path=str(entry_for_folder.get())
        if(file_path=="" or file_path[0]==" "):
            file_path=os.getcwd()
        files=[]
        # r=root, d=directories, f = files
        for r, d, f in os.walk(file_path):
            for file in f:
                file_str=file.lower()
                if((".mp4" in file_str) and ('.enc' not in file_str)):
                    direc = os.path.split(r)
                    cwd=os.path.join(cwd_original,direc[-1])
                    try:
                        os.mkdir(cwd)
                    except:
                        pass #Chill
                    input_file = open((os.path.join(r,file)),"rb")
                    input_data = input_file.read()
                    input_file.close()
                    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
                    enc_data = cfb_cipher.encrypt(input_data)
                    enc_file = open(os.path.join(cwd,file)+".enc", "wb")
                    enc_file.write(enc_data)
                    enc_file.close()
        root.destroy()
        root = Tk()
        root.title("Encryption Successfully Done")
        root.geometry("400x200")
        label = Label(text="Encryption Successfully Done", height=50, width=50, font=(None, 15))
        label.pack(anchor=CENTER, pady=50)
        root.mainloop()
    


def decrypt_video():
    try:
        os.mkdir(os.path.join(cwd_original_1,"Decrypted"))
    except:
        pass
    global key,iv,entry_for_folder,root
    file_path=str(entry_for_folder.get())
    if(file_path=="" or file_path[0]==" "):
        file_path=os.getcwd()
    files=[]
    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_path):
        for file in f:
            file_str=file.lower()
            if(".enc" in file_str):
                direc = os.path.split(r)
                cwd=os.path.join(cwd_original_decrypt,direc[-1])
                try:
                    os.mkdir(cwd)
                except:
                    pass #Chill
                enc_file = open((os.path.join(r,file)),"rb")
                enc_data = enc_file.read()
                enc_file.close()
                cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
                dec_data = cfb_decipher.decrypt(enc_data)
                dec_file = open(os.path.join(cwd,file[:-4]), "wb")
                dec_file.write(dec_data)
                dec_file.close()
    root.destroy()
    root = Tk()
    root.title("Decryption Successfully Done")
    root.geometry("400x200")
    label = Label(text="Decryption Successfully Done", height=50, width=50, font=(None, 15))
    label.pack(anchor=CENTER, pady=50)
    root.mainloop()


def decompress_video():
    # Open the compressed video file for reading
    cap = cv2.VideoCapture(compressed_file)

    # Get the video frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Get the video frame size
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a video writer object for the decompressed video file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(decompressed_file, fourcc, fps, (frame_width, frame_height), isColor=False)

    # Loop through the video frames
    while cap.isOpened():
        # Read the next frame
        ret, compressed_frame = cap.read()

        if ret == True:
            # Decompress the frame using IDWT
            decompressed_frame = pywt.idwt2((compressed_frame, (np.zeros_like(compressed_frame), np.zeros_like(compressed_frame), np.zeros_like(compressed_frame))), 'haar')

            # Convert the frame to unsigned 8-bit integers
            decompressed_frame = np.uint8(decompressed_frame)

            # Write the decompressed frame to the video writer object
            out.write(decompressed_frame)

        else:
            break

    # Release the video capture and writer objects
    cap.release()
    out.release()




   
root=Tk()

root.title("COMPRESSION_ENCRYPT_DECRYPT")

folder_directory_label=Label(text="Enter the Folder Directory")
folder_directory_label.pack()

entry_for_folder=Entry(root)
entry_for_folder.pack()


encrypt=Button(text="Compress/Encrypt All",command=compress_video)
encrypt.pack()
label=Label(text="Leave Blank for Current Working Directory")
label.pack()
decrypt=Button(text="DECRYPT/Decompress All",command=decompress_video)
decrypt.pack()




root.mainloop()