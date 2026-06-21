from db import DB
from tkinter import *
from tkinter import ttk,Canvas
from PIL import Image,ImageTk
import os
from constants import WIDTH,HEIGHT

class Platform:
    def __init__(self):
        db = DB()
        self.restaurants = []
        self.users = []
        self.current_user = []
        
    def Signup(self):
        pass
    def Signin(self):
        pass
    
    def Run(self):
        root = Tk()
        root.geometry(f'{WIDTH}x{HEIGHT}')
        root.resizable(False,False)
        
        img = Image.open(os.path.join(".","public","images","auth_section.jpg"))
        img = img.resize((WIDTH, HEIGHT))
        bg_img = ImageTk.PhotoImage(img)
        bg_label = Label(root,image=bg_img)
        bg_label.pack()
        
        form_frame = Frame(bg_label, bg="white")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        canvas = Canvas(form_frame, width=WIDTH, height=HEIGHT, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=bg_img, anchor="nw")

        # Title
        canvas.create_text(
            400, 120,
            text="Create Account",
            fill="#2cac2c",
            font=("Segoe", 32, "bold"),
        )

        # Username label + entry
        canvas.create_text(
            300, 220,
            text="Username",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        username_entry = Entry(form_frame, width=30)
        canvas.create_window(650, 220, window=username_entry)

        # Name label + entry
        canvas.create_text(
            300, 270,
            text="Name",
            fill="#222",
            font=("Segoe UI", 16, "bold")
        )

        name_entry = Entry(form_frame, width=30)
        canvas.create_window(650, 270, window=name_entry)

        # Password label + entry
        canvas.create_text(
            300, 320,
            text="Password",
            fill="#222",
            font=("Segoe UI", 16, "bold")
        )

        password_entry = Entry(form_frame, width=30, show="*")
        canvas.create_window(650, 320, window=password_entry)

        # Role label
        canvas.create_text(
            300, 370,
            text="Role",
            fill="#222",
            font=("Segoe UI", 16, "bold")
        )

        role_var = StringVar(value="Customer")
        role_menu = OptionMenu(form_frame, role_var, "Manager", "Customer")
        canvas.create_window(650, 370, window=role_menu)

        
        root.mainloop()