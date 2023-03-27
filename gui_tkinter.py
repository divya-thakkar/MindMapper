from tkinter import *
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo
from pygame import mixer

window = Tk()
window.title("Television")
# 16:9 aspect ratio for television
window.geometry("1200x675") 
window.configure(bg="black")
 
videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.load(r"./assets/iCarly_scene.mp4")
videoplayer.pack(expand=True, fill="both")

mixer.init()
mixer.music.load("./assets/iCarly_scene_compressed.mp3")

videoplayer.play()
mixer.music.play()

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


# center this label
#lbl1 = Label(window, text="Mind Mapper Sample Television", bg="black", fg="white", font="none 24 bold")
label = Label(window, text="Chinese TV", bg="black", fg="white", font="none 24 bold")
label.config(anchor=CENTER)
label.pack()

pause_btn = Button(window, text='Pause', width=14, bg='red', fg='black', command=lambda: pause_play())
pause_btn.pack()

volUp_btn = Button(window, text='Volume Up', command=lambda: playAgain())
volUp_btn.pack(side=TOP, pady=3)

volDown_btn = Button(window, text='Volume Down', command=lambda: StopVideo())
volDown_btn.pack(side=TOP, padx=4)

menu_btn = Button(window, text='Menu', command=lambda: PauseVideo())
menu_btn.pack(side=TOP, padx=5)

window.mainloop()