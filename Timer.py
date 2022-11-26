#countdown timer app
import tkinter as tk
from time import sleep
from tkinter import ttk, StringVar
from tkinter.messagebox import showinfo

def loadLastSetting():
    data=[]
    try:
        with open('time', 'r') as file:
            for line in file:
                data.append(line.rstrip("\n"))
            minutes=data[0]
            minutes=minutes[12:]
            seconds=data[1]
            seconds=seconds[12:]
            print(minutes,seconds)
            
    except OSError:
        createSettings()
        minutes=0
        seconds=0

    return minutes, seconds


def setDefaultSetting(minutes, seconds):
    data=[]
    with open('time', 'r') as file:
        for line in file:
                data.append(line)
        data[0]="lastMinutes="+str(minutes)+"\n"
        data[1]="lastSeconds="+str(seconds)+"\n"
    with open('time', 'w') as file:
                file.writelines(data)

def setPauseSetting(minutes, seconds):
    data=[]
    with open('time', 'r') as file:
        for line in file:
                data.append(line)
        data[2]="lastPauseMinutes="+str(minutes)+"\n"
        data[3]="lastPauseSeconds="+str(seconds)+"\n"
    with open('time', 'w') as file:
                file.writelines(data)

def loadPauseSetting():
    data=[]
    with open('time', 'r') as file:
        for line in file:
            data.append(line.rstrip("\n"))
        minutes=data[2]
        minutes=minutes[17:]
        seconds=data[3]
        seconds=seconds[17:]
    return int(minutes), int(seconds)

def createSettings():
    with open('time', 'w') as file:
        file.write("lastMinutes=0\n")
        file.write("lastSeconds=0\n")
        file.write("lastPauseMinutes=0\n")
        file.write("lastPauseSeconds=0")
        
def countdownPause():
    global isPaused
    
    if isPaused==False:
        pauseButton.configure(text="Resume")
        root.update()
        isPaused=True
    else:
        pauseButton.configure(text="Pause")
        root.update()
        isPaused=False
        minutes,seconds=loadPauseSetting()
        countdown(minutes,seconds)
        
def makeReadable(minutes, seconds):
    if seconds<10:
        return (f"{minutes}:0{seconds}")
    return (f"{minutes}:{seconds}")
            
def decrementSecond(minutes, seconds):
    if minutes>=1:
        if seconds==0:
            minutes-=1
            seconds=59          
    if seconds>0:
        seconds-=1       
    return minutes, seconds

def countdownStart():
    try:
        minutesGet=int(dropdownMinutes.get())
        secondsGet=int(dropdownSeconds.get())
        setDefaultSetting(minutesGet, secondsGet)
        countdown(minutesGet, secondsGet)
    except:
        tk.messagebox.showwarning("Error", "Please enter numbers only.")

def countdownPreset(minutes,seconds):
    countdown(minutes, seconds)
    
def countdown(minutes, seconds):
    global isPaused
    isPaused=False
    while minutes>=0 and seconds>=0:
        root.after(1000)
        if minutes==0 and seconds==0:
            tk.messagebox.showwarning("Timer", "Timer complete!")
            break
        if isPaused==False:
            minutes,seconds=decrementSecond(minutes, seconds) 
            readableTime=makeReadable(minutes, seconds)
            updateTimerLabel(readableTime)
        if isPaused==True:
            setPauseSetting(minutes,seconds)
            break

def updateTimerLabel(textString):
    labelCountdown.configure(text=textString)
    root.update()

def populateMenus():
    for i in range (1,12):
        minutesMenu.append(i*5)
    for i in range (1,4):
        secondsMenu.append(i*15)

timeRemaining=0
minutesMenu=[0,1,2,3,4]
secondsMenu=[]
isPaused=False

populateMenus()
minutes,seconds=loadLastSetting()

root=tk.Tk()
root.title("Timer")
root.attributes('-topmost', 1)
root.geometry="width=600"
labelCountdown=ttk.Label(root, text=timeRemaining, font=("",48))
labelMinutes=ttk.Label(root, text="Minutes:")
dropdownMinutes=ttk.Combobox(root, value=minutesMenu, width=10)
labelSeconds=ttk.Label(root, text="Seconds:")
dropdownSeconds=ttk.Combobox(root, value=secondsMenu, width=10)
dropdownMinutes.set(minutes)
dropdownSeconds.set(seconds)

labelCountdown.grid(columnspan=2)
labelMinutes.grid(row=2,column=0)
dropdownMinutes.grid(row=3,column=0)
labelSeconds.grid(row=2,column=1)
dropdownSeconds.grid(row=3,column=1)


startButton=ttk.Button(root, text="Start", command=lambda: countdownStart())
pauseButton=ttk.Button(root, text="Pause", command=lambda: countdownPause())
presetButton1=ttk.Button(root, text="Preset: 05:00", command=lambda: countdownPreset(5,0))
presetButton2=ttk.Button(root, text="Preset: 10:00", command=lambda: countdownPreset(10,0))
presetButton3=ttk.Button(root, text="Preset: 30:00", command=lambda: countdownPreset(30,0))
presetButton4=ttk.Button(root, text="Preset: 60:00", command=lambda: countdownPreset(60,0))

startButton.grid(row=5,column=0)
pauseButton.grid(row=5,column=1)
presetButton1.grid(row=6,column=0)
presetButton2.grid(row=6,column=1)
presetButton3.grid(row=7,column=0)
presetButton4.grid(row=7,column=1)

root.mainloop()



