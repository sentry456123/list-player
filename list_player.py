import tkinter
from tkinter import filedialog
import vlc

TITLE = "List Player"
LOOP_ENABLED = "Loop enabled"
LOOP_DISABLED = "Loop disabled"

music_list: list[str] = []
player: vlc.MediaListPlayer = vlc.MediaListPlayer()

window = tkinter.Tk()
window.title(TITLE)
window.geometry("600x400")

relief = tkinter.GROOVE

def update_display():
    display_music_list_text.set(str(music_list)
        .replace(",", "\n")
        .replace("[", "")
        .replace("]", "")
        .replace("'", ""))

def select_file():
    filenames = filedialog.askopenfilenames(title="Open files", initialdir="/")
    music_list.extend(filenames)
    update_display()

def clear():
    music_list.clear()
    update_display()
    
def play():
    player.set_media_list(vlc.MediaList(music_list))
    player.play()

def pause():
    player.pause()

def stop():
    player.stop()

def enable_loop():
    player.set_playback_mode(vlc.PlaybackMode.loop)
    display_loop_text.set(LOOP_ENABLED)

def disable_loop():
    player.set_playback_mode(vlc.PlaybackMode.default)
    display_loop_text.set(LOOP_DISABLED)

display_music_list_text = tkinter.StringVar()
display_music_list_label = tkinter.Label(window, textvariable=display_music_list_text, relief=relief)

control_frame = tkinter.Frame(window, relief=relief)
open_button = tkinter.Button(control_frame, text="Add files", command=select_file, relief=relief)
clear_button = tkinter.Button(control_frame, text="Clear", command=clear, relief=relief)
play_button = tkinter.Button(control_frame, text="Play", command=play, relief=relief)
pause_button = tkinter.Button(control_frame, text="Pause", command=pause, relief=relief)
stop_button = tkinter.Button(control_frame, text="Stop", command=stop, relief=relief)
enable_loop_button = tkinter.Button(control_frame, text="Enable loop", command=enable_loop, relief=relief)
disable_loop_button = tkinter.Button(control_frame, text="Disable loop", command=disable_loop, relief=relief)
display_loop_text = tkinter.StringVar()
display_loop_text.set(LOOP_DISABLED)
display_loop_label = tkinter.Label(control_frame, textvariable=display_loop_text, relief=relief)

display_music_list_label.grid(row=0, column=0)
control_frame.grid(row=1, column=0)
open_button.grid(row=0, column=0)
clear_button.grid(row=0, column=1)
play_button.grid(row=0, column=2)
pause_button.grid(row=0, column=3)
stop_button.grid(row=0, column=4)
enable_loop_button.grid(row=1, column=0)
disable_loop_button.grid(row=1, column=1)
display_loop_label.grid(row=1, column=2)
window.mainloop()