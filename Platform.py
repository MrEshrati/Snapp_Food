from db import DB
from tkinter import *
from tkinter import ttk,Canvas
from PIL import Image,ImageTk
import os
from constants import WIDTH,HEIGHT

class Platform:
    def __init__(self):
        db = DB()
        self.root = Tk()
        self.restaurants = []
        self.users = []
        self.current_user = []
        
    def Signup(self):
        pass
    def Signin(self):
        pass
    
    def mainFrame(self,main_frame,bg_img):
        canvas = Canvas(main_frame, width=WIDTH, height=HEIGHT, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        canvas.create_image(0, 0, image=bg_img, anchor="nw")
        
        canvas.create_text(
            420, 150,
            text="Snapp Food",
            fill="white",
            font=("Segoe UI", 40, "bold")
        )
        
        signup_btn = Button(
            main_frame,
            text="Sign Up",
            font=("Segoe UI", 18, "bold"),
            width=15,
            height=2,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            cursor="hand2",
            bd=0,
            command=self.SignupFrame
        )

        signin_btn = Button(
            main_frame,
            text="Sign In",
            font=("Segoe UI", 18, "bold"),
            width=15,
            height=2,
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            cursor="hand2",
            bd=0,
            command=self.SigninFrame,
        )
        
        canvas.create_window(250, 350, window=signup_btn)
        canvas.create_window(580, 350, window=signin_btn)
        main_frame.tkraise()
    
    def SigninFrame(self,signin_frame):
            pass
        
    def SignupFrame(self,signup_frame,bg_img):
        canvas = Canvas(signup_frame, width=WIDTH, height=HEIGHT, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=bg_img, anchor="nw")

        canvas.create_text(
            400, 120,
            text="Create Account",
            fill="#2cac2c",
            font=("Segoe", 32, "bold"),
        )

        canvas.create_text(
            300, 220,
            text="Username",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        username = Entry(signup_frame, width=30)
        canvas.create_window(500, 220, window=username)

        canvas.create_text(
            300, 270,
            text="Name",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        name = Entry(signup_frame, width=30)
        canvas.create_window(500, 270, window=name)

        canvas.create_text(
            300, 320,
            text="Password",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        password = Entry(signup_frame, width=30, show="*")
        canvas.create_window(500, 320, window=password)

        canvas.create_text(
            300, 370,
            text="Role",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        roles = StringVar(value="Customer")
        rolesMenu = OptionMenu(signup_frame, roles, "Manager", "Customer")
        canvas.create_window(500, 370, window=rolesMenu)

    
    def Run(self):
        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.resizable(False,False)
        
        img = Image.open(os.path.join(".","public","images","auth_section.png"))
        img = img.resize((WIDTH, HEIGHT))
        bg_img = ImageTk.PhotoImage(img)
        bgLabel = Label(self.root,image=bg_img)
        bgLabel.pack()
        
        main_frame = Frame(bgLabel)
        signin_frame = Frame(bgLabel)
        signup_frame = Frame(bgLabel)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        signin_frame.place(relx=0.5, rely=0.5, anchor="center")
        signup_frame.place(relx=0.5, rely=0.5, anchor="center")  
        
        self.mainFrame(main_frame,bg_img)      
                
        self.root.mainloop()