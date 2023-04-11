from tkinter import *
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo
from pygame import mixer
import process_face_inputs
import threading
import queue
import sys

def pause_play():
    if pause_btn["text"] == "Play":
        pause_btn["text"] = "Pause"
        pause_btn["bg"] = "red"
        mixer.music.unpause()
        videoplayer.play()
    else:
        pause_btn["text"] = "Play"
        pause_btn["bg"] = "green"
        mixer.music.pause()
        videoplayer.pause()

def mute_btn_colourChange():
    if mute_btn["text"] == "Mute":
        mute_btn["text"] = "Unmute"
        mute_btn["bg"] = "red"
    else:
        mute_btn["text"] = "Mute"
        mute_btn["bg"] = "white"

def updateVolumeMeter(currVolume):
    if (int(currVolume) < 1):
        volume_meter.config(image=vol0)
    elif (int(currVolume) > 0 and int(currVolume) <= 25):
        volume_meter.config(image=vol1)
    elif int(currVolume) >= 25 and int(currVolume) <= 50:
        volume_meter.config(image=vol2)
    elif int(currVolume) >= 50 and int(currVolume) <= 75:
        volume_meter.config(image=vol3)
    elif int(currVolume) >= 75 and int(currVolume) <= 100:
        volume_meter.config(image=vol4)

def volumeUp():
    currVolume = mixer.music.get_volume()
    mixer.music.set_volume(currVolume + 0.125)
    currVolume = mixer.music.get_volume()
    print("Volume: ", currVolume)
    updateVolumeMeter(currVolume*100)

def volumeDown():
    currVolume = mixer.music.get_volume()
    mixer.music.set_volume(currVolume - 0.125)
    currVolume = mixer.music.get_volume()
    print("Volume: ", currVolume)
    updateVolumeMeter(currVolume*100)

def muteVolume():
    global isMuted
    global prevVolume
    if not isMuted:
        currVolume = mixer.music.get_volume()
        prevVolume = currVolume
        mixer.music.set_volume(0)
        currVolume = mixer.music.get_volume()
        print("Volume Muted")
        print("Volume: ", currVolume)
        updateVolumeMeter(currVolume*100)
        isMuted = True
        mute_btn_colourChange()
    else:
        mixer.music.set_volume(prevVolume)
        currVolume = mixer.music.get_volume()
        print("Volume: ", currVolume)
        updateVolumeMeter(currVolume*100)
        isMuted = False
        mute_btn_colourChange()
          
def closeTV():
    print("Television will now be closed")
    mixer.music.stop()
    window.destroy()
    sys.exit(1)

def after_callback():
    try:
        message = process_face_inputs.main_queue.get(block=False)
    except queue.Empty:
        # let's try again later
        window.after(100, after_callback)
        return
    if (message=="Jaw Clench Detected"):
        volumeUp()
    elif (message=="Neck Flex Detected"):
        volumeDown()
    elif (message=="Mouth movement"):
        muteVolume()
    elif (message=="Head nod detected"):
        pause_play()

    window.after(100, after_callback)

if __name__ == '__main__':
    window = Tk()

    window.title("Television")
    # 16:9 aspect ratio for television
    window.geometry("1200x675") 
    window.configure(bg="black")

    videoplayer = TkinterVideo(master=window, scaled=True)
    videoplayer.load(r"./assets/audio_video/iCarly_scene.mp4")
    videoplayer.pack(expand=True, fill="both")

    mixer.init()
    mixer.music.load("./assets/audio_video/iCarly_scene_compressed.mp3")

    master_frame = Frame(window)
    master_frame.pack(side=RIGHT, padx=20)

    # center this label
    #lbl1 = Label(window, text="Mind Mapper Sample Television", bg="black", fg="white", font="none 24 bold")
    mainLabel = Label(window, text="Mind Mapper", bg="black", fg="white", font="none 24 bold")
    mainLabel.config(anchor=CENTER)
    mainLabel.pack()

    global vol0
    global vol1
    global vol2
    global vol3
    global vol4
    global isMuted
    isMuted = False
    global prevVolume
    prevVolume = 0.625
    vol0 = PhotoImage(file='./assets/images/volume0.png')
    vol1 = PhotoImage(file='./assets/images/volume1.png')
    vol2 = PhotoImage(file='./assets/images/volume2.png')
    vol3 = PhotoImage(file='./assets/images/volume3.png')
    vol4 = PhotoImage(file='./assets/images/volume4.png')

    # Create Volume Meter
    mixer.music.set_volume(0.625)
    volume_meter = Label(master_frame, image=vol3)
    volume_meter.pack(side=RIGHT)
    '''
    volumeLabel = Label(master_frame, text="Volume: 62.5%", bg="black", fg="white", font="none 24 bold")
    volumeLabel.pack(side=RIGHT, row=1, col=0)
    '''

    videoplayer.play()
    mixer.music.play()

    pause_btn = Button(window, text='Pause', width=14, bg='red', fg='black', command=lambda: pause_play())
    pause_btn.pack(pady=5)

    volUp_btn = Button(window, text='Volume Up', command=lambda: volumeUp())
    volUp_btn.pack(side=TOP, padx=5)

    volDown_btn = Button(window, text='Volume Down', command=lambda: volumeDown())
    volDown_btn.pack(side=TOP, padx=5)

    mute_btn = Button(window, text='Mute', command=lambda: muteVolume())
    mute_btn.pack(side=TOP, padx=5, pady=5)

    exit_btn = Button(window, text='Exit', command=lambda: closeTV())
    exit_btn.pack(side=TOP, padx=5, pady=5)

    threading.Thread(target = process_face_inputs.detect_mouth_and_headnods).start()
    window.after(100, after_callback)

    window.mainloop()