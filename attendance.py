import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3
logo_path = os.path.join("UI_Image", "0001.png")
logo = Image.open(logo_path)
# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

#

def add_hover_effect(widget, hover_bg, hover_fg, default_bg, default_fg):
    widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg, fg=hover_fg))
    widget.bind("<Leave>", lambda e: widget.config(bg=default_bg, fg=default_fg))

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "./TrainingImageLabel/Trainner.yml"
)
trainimage_path = "/TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = (
    "./StudentDetails/studentdetails.csv"
)
attendance_path = "Attendance"

window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="#1c1c1c")  # Dark theme

img_path = r"UI_Image\space.jfif"
pil_img = Image.open(img_path)

# Resize image to fit window
pil_img = pil_img.resize((1500, 1000), Image.Resampling.LANCZOS)

bg_img = ImageTk.PhotoImage(pil_img)

# Create a label with the image and place it as background
bg_label = tk.Label(window, image=bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",  # Dark background for the error window
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",  # Darker button color
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


#logo = Image.open(r"UI_Image\0001.png")
logo = logo.resize((50, 47), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
titl = tk.Label(window, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1, bg="#1c1c1c",)
l1.place(x=470, y=10)


title_frame = tk.Frame(
    window,
    bg="white",
    bd=4,
    relief="raised",
)

# Use relx=0.5 to center horizontally, anchor='n' aligns top center
title_frame.place(relx=0.5, y=10, anchor='n')

# Title label inside the frame
titl = tk.Label(
    title_frame,
    text="AI Attendance",
    bg="white",
    fg="#1a1a1a",
    font=("Verdana", 26, "bold"),
    padx=20,
    pady=10,
)
titl.pack()




icon_width, icon_height = 104, 104
icon_spacing = 380  # space between icons
num_icons = 3

# Total width needed for layout
total_width = (icon_width * num_icons) + (icon_spacing * (num_icons - 1))
window_width = 1400  # Adjust based on your actual window size
start_x = (window_width - total_width) // 2
y_pos = 270  # Vertical position of icons

# Load and place icons with loop-style layout
icon_paths = [
    "UI_Image/register.jpg",
    "UI_Image/verifyy.jpg",
    "UI_Image/attendance.webp"
]
icons = []

for i, path in enumerate(icon_paths):
    img = Image.open(path)
    img = img.resize((icon_width, icon_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(window, image=photo)
    label.image = photo
    label.place(x=start_x + i * (icon_width + icon_spacing), y=y_pos)
    icons.append(label)


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")  # Dark background for the image window
    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)
    # image and title
    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="#1c1c1c", fg="green", font=("Verdana", 30, "bold"),
    )
    titl.place(x=270, y=12)

    # heading
    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#1c1c1c",  # Dark background for the details label
        fg="yellow",  # Bright yellow text color
        bd=10,
        font=("Verdana", 24, "bold"),
    )
    a.place(x=280, y=75)

    # ER no
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="#333333",  # Dark input background
        fg="yellow",  # Bright text color for input
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#333333",  # Dark input background
        fg="yellow",  # Bright text color for input
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="#333333",  # Dark background for messages
        fg="yellow",  # Bright text color for messages
        relief=RIDGE,
        font=("Verdana", 14, "bold"),
    )
    message.place(x=250, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",  # Dark background for the button
        fg="yellow",  # Bright text color for the button
        height=2,
        width=12,
        relief=RIDGE,
    )
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # train Image function call
    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",  # Dark background for the button
        fg="yellow",  # Bright text color for the button
        height=2,
        width=12,
        relief=RIDGE,
    )
    trainImg.place(x=360, y=350)


r = tk.Button(
    window,
    text="Register Student",
    command=TakeImageUI,
    bd=10,
    font=("Verdana", 16),
    bg="white",
    fg="black",
    height=2,
    width=17,
)
r.place(x=100, y=520)
add_hover_effect(r, hover_bg="blue", hover_fg="white", default_bg="white", default_fg="black")


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


r = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attedance,
    bd=10,
    font=("Verdana", 16),
    bg="white",
    fg="black",
    height=2,
    width=17,
)
r.place(x=600, y=520)
add_hover_effect(r, hover_bg="blue", hover_fg="white", default_bg="white", default_fg="black")


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


r = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    bd=10,
    font=("Verdana", 16),
    bg="white",
    fg="black",
    height=2,
    width=17,
)
r.place(x=1000, y=520)
add_hover_effect(r, hover_bg="blue", hover_fg="white", default_bg="white", default_fg="black")

r = tk.Button(
    window,
    text="EXIT",
    bd=10,
    command=quit,
    font=("Verdana", 16),
    bg="white",
    fg="black",
    height=2,
    width=17,
)
r.place(x=600, y=660)
add_hover_effect(r, hover_bg="blue", hover_fg="white", default_bg="white", default_fg="black")


window.mainloop()
