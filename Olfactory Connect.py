print("\n\n\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n")
print("\nWelcome\n")
print("The Olfactory Connect GUI will open shortly.")
print("When the program opens, please leave this terminal window open.")
print("It will attempt to connect to the mBot2 automatically.")
print("If the connection was successful, ")
print("\tthe mBot2 will play a bell noise.")
print("If the connection was unsuccessful, ")
print("\tsimply click the \"connect\" button in the application window.")
print("\n\n/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\n")

import time, os, csv, customtkinter, threading
import tkinter as tk
from cyberpi import *
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import filedialog

#List to hold all data to be written to CSV file.
compiledLIST = []

#Variable to stop the robot from functioning.
stopRobot = False

#Write all necessary data to the CSV file called myData.csv.
def saveDataFile():
    filePath = filedialog.asksaveasfilename(defaultextension='.csv')
    with open(filePath, mode='w') as csvfile:
        fieldnames = ['Current_Time', 'Distance_From_Fan_mm', 'Closeness_Score', 'Delta_Distance', 'Fan_Speed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(compiledLIST)

#Function to connect to the makebot device.
def getConnected():
    cyberpi.display.clear()
    cyberpi.console.println('Connected!')
    cyberpi.audio.play("glass-clink")
    cyberpi.led.off(id = "all")
    startButton.configure(state="normal")
    startButton.configure(fg_color="green")
    connectButton.configure(text="Connected")
    connectButton.configure(fg_color="grey")
    connectButton.configure(state="disabled")
    mbot2.EM_set_power(0, "EM2")

def stopRunning():
    global stopRobot
    stopRobot = True
    startButton.configure(command=startGetStartedThread)
    startButton.configure(fg_color="green")
    startButton.configure(text="Start")
    distanceText.configure(text="Stopped")
    speedText.configure(text="Stopped")
    speedText.configure(fg_color="white")
    closenessBar.start()
    mbot2.EM_set_power(0, "EM2")
    showFileButton.configure(state="normal")
    showFileButton.configure(fg_color="green")

#Function that triggers the start of a session with the makebot device. Stops the GUI from updating while running.
def getStarted():
    global stopRobot
    stopRobot = False
    startButton.configure(text="Stop")
    startButton.configure(fg_color="red")
    startButton.configure(command=stopRunning)
    closenessBar.stop()
    closenessBar.set(0)

    time.sleep(1)

    while (stopRobot == False):
        cyberpi.display.clear()
        distanceOfPlayer = ultrasonic2.get(index = 1)
        lastDistance = 0
        deltaDistance = distanceOfPlayer - lastDistance

        while (stopRobot == False):
            distanceOfPlayer = ultrasonic2.get(index = 1)

            #Speed 1 (Player is closest)
            if ((distanceOfPlayer > 5) and (distanceOfPlayer < 11) and (stopRobot == False)):
                mbot2.EM_set_power(-6, "EM2")
                distanceText.configure(text=distanceOfPlayer)
                speedText.configure(text="6")
                speedText.configure(fg_color="white")
                closenessBar.set(0.2)
                deltaDistance = distanceOfPlayer - lastDistance
                if((deltaDistance < 30) and (deltaDistance > -30)):
                    compiledLIST.append({"Current_Time": datetime.now(), "Distance_From_Fan_mm": distanceOfPlayer, "Closeness_Score": "1: Closest", "Delta_Distance": deltaDistance, "Fan_Speed": 10})
                lastDistance = distanceOfPlayer
                distanceOfPlayer = ultrasonic2.get(index = 1)
            
            #Speed 2
            if ((distanceOfPlayer > 10) and (distanceOfPlayer < 21) and (stopRobot == False)):
                mbot2.EM_set_power(-10, "EM2")
                distanceText.configure(text=distanceOfPlayer)
                speedText.configure(text="10")
                speedText.configure(fg_color="yellow")
                closenessBar.set(0.4)
                deltaDistance = distanceOfPlayer - lastDistance
                if((deltaDistance < 30) and (deltaDistance > -30)):
                    compiledLIST.append({"Current_Time": datetime.now(), "Distance_From_Fan_mm": distanceOfPlayer, "Closeness_Score": "2: Very Close", "Delta_Distance": deltaDistance, "Fan_Speed": 20})
                lastDistance = distanceOfPlayer
                distanceOfPlayer = ultrasonic2.get(index = 1)

            #Speed 3
            if ((distanceOfPlayer > 21) and (distanceOfPlayer < 31) and (stopRobot == False)):
                mbot2.EM_set_power(-20, "EM2")
                distanceText.configure(text=distanceOfPlayer)
                speedText.configure(text="20")
                speedText.configure(fg_color="yellow")
                closenessBar.set(0.6)
                deltaDistance = distanceOfPlayer - lastDistance
                if((deltaDistance < 30) and (deltaDistance > -30)):
                    compiledLIST.append({"Current_Time": datetime.now(), "Distance_From_Fan_mm": distanceOfPlayer, "Closeness_Score": "3: Medium", "Delta_Distance": deltaDistance, "Fan_Speed": 40})
                lastDistance = distanceOfPlayer
                distanceOfPlayer = ultrasonic2.get(index = 1)

            #Speed 4
            if ((distanceOfPlayer > 31) and (distanceOfPlayer < 41) and (stopRobot == False)):
                mbot2.EM_set_power(-40, "EM2")
                distanceText.configure(text=distanceOfPlayer)
                speedText.configure(text="40")
                speedText.configure(fg_color="orange")
                closenessBar.set(0.8)
                deltaDistance = distanceOfPlayer - lastDistance
                if((deltaDistance < 30) and (deltaDistance > -30)):
                    compiledLIST.append({"Current_Time": datetime.now(), "Distance_From_Fan_mm": distanceOfPlayer, "Closeness_Score": "4: Pretty Far", "Delta_Distance": deltaDistance, "Fan_Speed": 60})
                lastDistance = distanceOfPlayer
                distanceOfPlayer = ultrasonic2.get(index = 1)

            #Speed 5 (Player is furthest)
            if ((distanceOfPlayer > 40) and (distanceOfPlayer < 100) and (stopRobot == False)):
                mbot2.EM_set_power(-60, "EM2")
                distanceText.configure(text=distanceOfPlayer)
                speedText.configure(text="60")
                speedText.configure(fg_color="red")
                closenessBar.set(1)
                deltaDistance = distanceOfPlayer - lastDistance
                if((deltaDistance < 30) and (deltaDistance > -30)):
                    compiledLIST.append({"Current_Time": datetime.now(), "Distance_From_Fan_mm": distanceOfPlayer, "Closeness_Score": "5: Furthest", "Delta_Distance": deltaDistance, "Fan_Speed": 80})
                lastDistance = distanceOfPlayer
                distanceOfPlayer = ultrasonic2.get(index = 1)

            #Safety (the sensor reads 300 when you get right up next to it. This will disable the fan.)
            if ((distanceOfPlayer > 200) and (distanceOfPlayer < 400) and (stopRobot == False)):
                mbot2.EM_set_power(0, "EM2")
                distanceText.configure(text=distanceOfPlayer)
                speedText.configure(text="0")
                speedText.configure(fg_color="white")
                closenessBar.set(0)
                deltaDistance = distanceOfPlayer - lastDistance
                if((deltaDistance < 30) and (deltaDistance > -30)):
                    compiledLIST.append({"Current_Time": datetime.now(), "Distance_From_Fan_mm": distanceOfPlayer, "Closeness_Score": "5: Furthest", "Delta_Distance": deltaDistance, "Fan_Speed": 80})
                lastDistance = distanceOfPlayer
                distanceOfPlayer = ultrasonic2.get(index = 1)
                

#Creates a new thread to handle the robot. Interface runs on the main thread. Creates a new thread each time you click "Start".
def startGetStartedThread():
    global getStartedTHREAD
    getStartedTHREAD = threading.Thread(target=getStarted)
    getStartedTHREAD.start()

#User Interface Settings.
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("460x500")
app.title("Olfactory Connect")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)
app.resizable(0,0)
# ico = Image.open("./Picture1.ico")
# photo = ImageTk.PhotoImage(ico)
# app.wm_iconphoto(False, photo)

mainFrame = customtkinter.CTkFrame(master=app, width=900, height=360, fg_color="transparent")
mainFrame.grid(row=0, column=0, sticky="nsew")
mainFrame.pack(padx=20, pady=20)

connectButton = customtkinter.CTkButton(mainFrame, text="Connect", state="normal", hover=True, fg_color='blue', command=getConnected)
connectButton.pack(padx=10, pady=10)

startButton = customtkinter.CTkButton(mainFrame, text="Start", state="disabled", hover=True, fg_color='grey', command=startGetStartedThread)
startButton.pack(padx=10, pady=10)

dashboardFrame = customtkinter.CTkFrame(master=mainFrame, width=100, height=100)
dashboardFrame.pack()

distanceFrame = customtkinter.CTkFrame(master=dashboardFrame, width=100, height=100, fg_color="black", corner_radius=4)
distanceFrame.pack(padx=10, pady=10)

distanceLabel = customtkinter.CTkLabel(distanceFrame, text="Distance: ", fg_color="transparent")
distanceLabel.pack(padx=5, pady=5)

distanceText = customtkinter.CTkLabel(distanceFrame, text="Current Distance", text_color="black", fg_color="white", corner_radius=0, width=100, height=25, font=("railway", 10))
distanceText.pack(padx=10, pady=10)

speedFrame = customtkinter.CTkFrame(master=dashboardFrame, width=100, height=100, fg_color="black", corner_radius=4)
speedFrame.pack(padx=10, pady=10)

speedLabel = customtkinter.CTkLabel(speedFrame, text="Fan Speed: ", fg_color="transparent")
speedLabel.pack(padx=5, pady=5)

speedText = customtkinter.CTkLabel(speedFrame, text="Current Speed", text_color="black", fg_color="white", corner_radius=0, width=100, height=25, font=("railway", 10))
speedText.pack(padx=10, pady=10)

closenessBar = customtkinter.CTkProgressBar(mainFrame, orientation = "horizontal")
closenessBar.pack(padx=10, pady=10)

closenessBar.start()

showFileButton = customtkinter.CTkButton(app, text="Save File", state="disabled", hover=True, fg_color='grey', command=saveDataFile)
showFileButton.pack(padx=10, pady=10)

lastOpenedText = customtkinter.CTkLabel(app, text="")
lastOpenedText.pack()

#Opens the save file (if it exists), reads the date last opened, and prints it to the console.
if os.path.isfile('./save.txt'):
    with open('./save.txt', 'r') as f:
        tempVariable = f.read()
        lastOpenedText.configure(text="Last opened: " + tempVariable)

#Try to connect automatically at startup.
@cyberpi.event.start
def callback():
    getConnected()

#Causes the window to open.
app.mainloop()

#Save the current date and time as the date last opened.
with open('save.txt', 'w') as f:
    f.write(str(datetime.now()))