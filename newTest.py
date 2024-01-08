import time, os, csv, customtkinter, threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog

startScreen = customtkinter.CTk()
startScreen.title("Looking for Cyberpi")
startScreen.grid_rowconfigure(0, weight=1)
startScreen.grid_columnconfigure(0, weight=1)
startScreen.mainloop()
time.sleep(5)
from cyberpi import *
startScreen.destroy()



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

        distanceOfPlayer = ultrasonic2.get(index = 1)
        lastDistance = 0
        deltaDistance = distanceOfPlayer - lastDistance

        while (stopRobot == False):
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

mainFrame = customtkinter.CTkFrame(master=app, width=900, height=360, fg_color="transparent")
mainFrame.grid(row=0, column=0, sticky="nsew")
mainFrame.pack(padx=20, pady=20)

connectButton = customtkinter.CTkButton(mainFrame, text="Connect", state="normal", hover=True, fg_color='blue')
connectButton.pack(padx=10, pady=10)

startButton = customtkinter.CTkButton(mainFrame, text="Start", state="disabled", hover=True, fg_color='grey', command=startGetStartedThread)
startButton.pack(padx=10, pady=10)

dashboardFrame = customtkinter.CTkFrame(master=mainFrame, width=100, height=100)
dashboardFrame.pack()

distanceFrame = customtkinter.CTkFrame(master=dashboardFrame, width=100, height=100, fg_color="black", corner_radius=4)
distanceFrame.pack(padx=10, pady=10)

distanceLabel = customtkinter.CTkLabel(distanceFrame, text="Distance", text_color="white", fg_color="transparent")
distanceLabel.pack(padx=5, pady=5)

distanceText = customtkinter.CTkLabel(distanceFrame, text="Current Distance", text_color="black", fg_color="white", corner_radius=0, width=100, height=25, font=("railway", 10))
distanceText.pack(padx=10, pady=10)

speedFrame = customtkinter.CTkFrame(master=dashboardFrame, width=100, height=100, fg_color="black", corner_radius=4)
speedFrame.pack(padx=10, pady=10)

speedLabel = customtkinter.CTkLabel(speedFrame, text="Fan Speed", text_color="white", fg_color="transparent")
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

#Causes the window to open.
app.mainloop()

#Save the current date and time as the date last opened.
with open('save.txt', 'w') as f:
    f.write(str(datetime.now()))