from tkinter import *
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo

window = Tk()
window.title("Television")
# 16:9 aspect ratio for television
window.geometry("1200x675") 
window.configure(bg="black")
 
videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.load(r"iCarly_scene.mp4")
videoplayer.pack(expand=True, fill="both")
 
videoplayer.play()

def playAgain():
    print("Video Played")
    videoplayer.play()

def StopVideo():
    print("Video Stopped")
    videoplayer.stop()

def PauseVideo():
    print("Video Paused")
    videoplayer.pause()
    

# center this label
lbl1 = Label(window, text="Mind Mapper Sample Television", bg="black", fg="white", font="none 24 bold")
lbl1.config(anchor=CENTER)
lbl1.pack()

playbtn = Button(window, text='Play Video', command=lambda: playAgain())
playbtn.pack(side=TOP, pady=3)

stopbtn = Button(window, text='Stop Video', command=lambda: StopVideo())
stopbtn.pack(side=TOP, padx=4)

pausebtn = Button(window, text='Pause Video', command=lambda: PauseVideo())
pausebtn.pack(side=TOP, padx=5)

window.mainloop()