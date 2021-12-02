#! python3

#Import the modules I need
import os
import shutil
import sys
from datetime import *
from tkinter import *
import getpass

r"""
NOTE: While this program does get rid of user temporary files located in 
C:\Users\Usename\Appdata\Local\Temp, it will not touch the C:\Windows\Temp directory. 
That requires Administrator access and I do not want this program to be a security risk for your 
system.
"""


# This is to get the username of the current user running the program
uname = getpass.getuser()

# Removes files and directories
def rmdirs(path):
    for filename in os.listdir():
        shutil.rmtree(str(path), ignore_errors = True) # Setting ignore_errors to True helps us know what was and wasn't deleted without stopping the program

# This function will write a log that will continuously get appended to with files that weren't deleted
def logwriter():
    # We need to change directories as the program will go to C:\Users\Username\AppData\Local\Temp
    os.chdir(rf'C:\Users\{uname}\Desktop')
    with open('Templog.txt', 'a+') as logfile:
        logfile.write('\n' + '-' * 50)
        for filename in os.listdir(rf'C:\Users\{uname}\AppData\Local\Temp'):
            logfile.write("\nDate: " + str(datetime.now()) + "\n\t'%s' was not deleted"% filename)

# This function will update the list box after the deletion
def update():
    lb1.delete(0, END)
    for filename in os.listdir(rf'C:\Users\{uname}\AppData\Local\Temp'):
        # Populate the Listbox with an filename and always append it to the end of the Listbox
        lb1.insert(END, filename)

# Temp directory deletion entry function   
def main():
    rmdirs(rf'C:\Users\{uname}\AppData\Local\Temp')
    logwriter()
    update()

if __name__ == '__main__':
    # Changing the current working directory of the application to users %temp% directory
    try:
        os.chdir(rf'C:\Users\{uname}\AppData\Local\Temp')
    except FileNotFoundError as e:
        from tkinter import messagebox
        messagebox.showerror(title="Error", message=f"The user's temp directory was not found. Please create the directory or go online for troubleshooting solutions\nError Encountered: {e}")
        # ctypes.windll.user32.MessageBoxW(0, f"The user's temp directory was not found. Please create the directory or go online for troubleshooting solutions\nError Encountered: {e}", "Error", 0)
        sys.exit(1)
    
    # A starting bookmark of all the files in the temp directory
    templist = os.listdir()

    # Start main window
    w = Tk()
    frame = Frame(w)
    frame.pack()

    # Setting the windows Title
    w.title('Windows Temp File Eraser')

    # Creating a Lable to show where the program's current working directory is
    L1 = Label(frame, text = f'Now in {os.getcwd()}')
    L1.pack()

    # Listbox of all files in the users temp directory
    lb1 = Listbox(frame, width = 50, height = 12)
    lb1.insert(END, *templist) # We place an * to tell tkinter to use the entire list
    lb1.pack(side = LEFT, fill = X)

    # Setting up the Scrollbar for the Listbox
    sb1 = Scrollbar(frame)
    sb1.pack(side = LEFT, fill = Y)

    # Configuring the Scrollbar to interact with the Listbox
    lb1.configure(yscrollcommand = sb1.set)
    sb1.configure(command = lb1.yview)

    # Creating the button to use the main function
    b1 = Button(frame, text = 'Delete', command = main)
    b1.pack(side = TOP, pady = 5)

    # Configuring the quit program button
    b2 = Button(frame, text = 'Quit', command = sys.exit)
    b2.pack(side = TOP)

    # Starting the GUI
    w.mainloop()
