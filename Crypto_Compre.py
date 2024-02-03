from tkinter import *
import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo


def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration


def update_scale(event):
    """ updates the scale value """
    progress_value.set(vid_player.current_duration())


def load_video():
    """ loads the video """
    global file_path
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)
        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)


def seek(value):
    """ used to seek a specific timeframe """
    vid_player.seek(int(value))


def skip(value: int):
    """ skip seconds """
    vid_player.seek(int(progress_slider.get()) + value)
    progress_value.set(progress_slider.get() + value)


def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"


def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)

def encrypt_vid() :
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)
        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)

def decrypt_vid():
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)
        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)
def compress_vid():
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)
        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)

def decompress_vid():
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)
        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)


window = tk.Tk()
window.geometry("900x500+290+10")
window.title("Crypto / Compression video")
window.configure(background='skyblue')

frame = tk.Frame(window, bg='grey')
frame.pack(padx=15, pady=15, )
frame1 = tk.Frame(window, width=750, height=500, bg='grey')
frame1.pack(fill='both', padx=10, pady=5, expand=True)

left_frame = tk.Frame(frame1, width=600, height=500, bg='grey')
left_frame.pack(side='left', fill='both', padx=10, pady=5, expand=True)

tool_bar = tk.Frame(frame1, width=90, height=185, bg='lightgrey')
tool_bar.pack(side='left', fill='both', padx=5, pady=5, expand=True)

title = tk.Label(master=frame, text='APPLICATION POUR LA COMPRESSION ET LE CRYPTAGE DES VIDEOS', font='Calibri 15 bold')
title.pack(pady=5)

tk.Button(tool_bar, text="SELECTIONNER UNE VIDEO", command=load_video).pack(padx=10, pady=5)
tk.Button(tool_bar, text="COMPRESSER LA VIDEO", command=lambda: compress_vid()).pack(padx=10, pady=5)
tk.Button(tool_bar, text="CRYPTER LA VIDEO", command=lambda: encrypt_vid()).pack(padx=10, pady=5)
tk.Button(tool_bar, text="DECRYPTER LA VIDEO", command=lambda: decrypt_vid()).pack(padx=10, pady=5)
tk.Button(tool_bar, text="DECOMPRESSER LA VIDEO", command=lambda: decompress_vid()).pack(padx=10, pady=5)

img_original = tk.Label(master=left_frame, text='AFFICHAGE DU VIDEO', font='Calibri 15 bold')
img_original.pack(pady=5)

vid_player = TkinterVideo(left_frame, scaled=True)
vid_player.pack(expand=True, fill="both")

lower_frame = tk.Frame(left_frame, bg="#FFFFFF")
lower_frame.pack(fill="both", side=BOTTOM)

play_pause_btn = tk.Button(lower_frame, text="Play", width=30, height=2, command=play_pause)
play_pause_btn.pack(expand=True, fill="both", side=LEFT)

start_time = tk.Label(lower_frame, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side="left")

progress_value = tk.IntVar(left_frame)

progress_slider = tk.Scale(lower_frame, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
progress_slider.pack(side="left", fill="x", expand=True)

end_time = tk.Label(lower_frame, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side="left")

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended)

window.mainloop()