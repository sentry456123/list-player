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

fullscreen = False

relief = tkinter.GROOVE

volume = 50

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def update_music_list_text():
    music_list_text.set(str(music_list)
        .replace(",", "\n")
        .replace("[", "")
        .replace("]", "")
        .replace("'", ""))

def select_file():
    filenames = filedialog.askopenfilenames(title="Open files", initialdir="/")
    music_list.extend(filenames)
    update_music_list_text()

def clear():
    music_list.clear()
    update_music_list_text()
    
def play():
    player.set_media_list(vlc.MediaList(music_list))
    player.play()
    player.get_media_player().audio_set_volume(volume)

def pause():
    player.pause()

def stop():
    player.stop()

def enable_loop():
    player.set_playback_mode(vlc.PlaybackMode.loop)
    loop_text.set(LOOP_ENABLED)

def disable_loop():
    player.set_playback_mode(vlc.PlaybackMode.default)
    loop_text.set(LOOP_DISABLED)

def volume_up():
    global volume
    volume += 10
    volume = clamp(volume, 0, 100)
    player.get_media_player().audio_set_volume(volume)
    volume_text.set(str(volume) + "%")

def volume_down():
    global volume
    volume -= 10
    volume = clamp(volume, 0, 100)
    player.get_media_player().audio_set_volume(volume)
    volume_text.set(str(volume) + "%")

def on_key_press(event: tkinter.Event):
    global fullscreen
    c = event.keysym
    c = c.lower()
    ctrl = (event.state & 0x4) != 0
    
    match c:
        case 'escape':
            fullscreen = False
            window.attributes("-fullscreen", fullscreen)
        case 'f11':
            fullscreen = not fullscreen
            window.attributes("-fullscreen", fullscreen)
    if not ctrl:
        return
    match c:
        case 'a': play()
        case 's': pause()
        case 'd': stop()
        case 'e': select_file()
        case 'z': enable_loop()
        case 'x': disable_loop()
        case 'c': volume_up()
        case 'v': volume_down()
        case 'w': window.destroy()
        case 'f':
            fullscreen = not fullscreen
            window.attributes("-fullscreen", fullscreen)

music_list_text = tkinter.StringVar()
music_list_label = tkinter.Label(window, textvariable=music_list_text, relief=relief)

main_control_frame = tkinter.Frame(window, relief=relief)
open_button = tkinter.Button(main_control_frame, text="Add files", command=select_file, relief=relief)
clear_button = tkinter.Button(main_control_frame, text="Clear", command=clear, relief=relief)
play_button = tkinter.Button(main_control_frame, text="Play", command=play, relief=relief)
pause_button = tkinter.Button(main_control_frame, text="Pause", command=pause, relief=relief)
stop_button = tkinter.Button(main_control_frame, text="Stop", command=stop, relief=relief)

loop_control_frame = tkinter.Frame(window, relief=relief)
enable_loop_button = tkinter.Button(loop_control_frame, text="Enable loop", command=enable_loop, relief=relief)
disable_loop_button = tkinter.Button(loop_control_frame, text="Disable loop", command=disable_loop, relief=relief)
loop_text = tkinter.StringVar()
player.set_playback_mode(vlc.PlaybackMode.default)
loop_text.set(LOOP_DISABLED)
loop_label = tkinter.Label(loop_control_frame, textvariable=loop_text, relief=relief)

volume_control_frame = tkinter.Frame(window, relief=relief)
volume_up_buttom = tkinter.Button(volume_control_frame, text="Volume up", command=volume_up, relief=relief)
volume_down_buttom = tkinter.Button(volume_control_frame, text="Volume down", command=volume_down, relief=relief)
volume_text = tkinter.StringVar()
volume_text.set(str(volume) + "%")
volume_label = tkinter.Label(volume_control_frame, textvariable=volume_text, relief=relief)

music_list_label.grid(row=0, column=0)
main_control_frame.grid(row=1, column=0)
volume_control_frame.grid(row=3, column=0)
loop_control_frame.grid(row=2, column=0)

open_button.grid(row=0, column=0)
clear_button.grid(row=0, column=1)
play_button.grid(row=0, column=2)
pause_button.grid(row=0, column=3)
stop_button.grid(row=0, column=4)

enable_loop_button.grid(row=0, column=0)
disable_loop_button.grid(row=0, column=1)
loop_label.grid(row=0, column=2)

volume_up_buttom.grid(row=0, column=0)
volume_down_buttom.grid(row=0, column=1)
volume_label.grid(row=0, column=2)

window.bind("<Key>", on_key_press)

window.mainloop()
