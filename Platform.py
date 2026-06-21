from db import DB
from User import User
from tkinter import *
from tkinter import ttk,Canvas
from PIL import Image,ImageTk
import os
from constants import WIDTH,HEIGHT

class Platform:
    def __init__(self):
        self.db = DB()
        self.root = Tk()
        self.restaurants = []
        self.users = [
            {"_id": "c1", "name": "Arshia", "username": "AAA", "password": "AAA111"},
            {"_id": "c2", "name": "Arshia", "username": "BBB", "password": "BBB222"},
            {"_id": "m1", "name": "Arshia", "username": "CCC", "password": "CCC333"},
        ]
        self.current_user = []
        
        img = Image.open(os.path.join(".","public","images","auth_section.png"))
        img = img.resize((WIDTH, HEIGHT))
        self.bg_img = ImageTk.PhotoImage(img)
        bgLabel = Label(self.root,image=self.bg_img)
        bgLabel.pack()
        
        self.main_frame = Frame(bgLabel)
        self.signin_frame = Frame(bgLabel)
        self.signup_frame = Frame(bgLabel)
        
    def Signup(self,name,username,password,role):
        
        user = User(name,username,password)
        validation = True
        if(user.checkName()):
            if(user.checkUsername(self.users)):
                if(user.checkPassword()):
                    user.createId(role,self.users)
                else:
                    validation = False
                    print("Password is not valid(must be 8 or more characters)")
            else:
                validation = False
                print("Username is not valid(must be 5 or more letters and unique)")
        else:
            validation = False
            print("Name is not valid(must be 5 or more letters)")
                    
        if(validation):
            self.db.PostData("Users",{
                "_id": user._id,
                "name": user.name,
                "username": user.username,
                "password": user.password,
            })
        
            self.main_frame.tkraise()
    def Signin(self):
        pass
       
    def SigninFrame(self):
            pass
        
    def CreateSignupFrame(self):
        canvas = Canvas(self.signup_frame, width=WIDTH, height=HEIGHT, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        
        backBtn = Button(
            self.signup_frame,
            text="← Back",
            font=("Segoe UI", 12, "bold"),
            bg="#555555",
            fg="white",
            activebackground="#444444",
            bd=0,
            cursor="hand2",
            command=lambda: self.main_frame.tkraise()
        )
        canvas.create_window(50, 50, window=backBtn)


        canvas.create_text(
            420, 115,
            text="Create Account",
            fill="#2cac2c",
            font=("Segoe", 32, "bold"),
        )


        canvas.create_text(
            300, 215,
            text="Name",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        name = Entry(self.signup_frame, width=30)
        canvas.create_window(500, 220, window=name)

        canvas.create_text(
            300, 265,
            text="Username",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        username = Entry(self.signup_frame, width=30)
        canvas.create_window(500, 270, window=username)
        
        canvas.create_text(
            300, 315,
            text="Password",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )

        password = Entry(self.signup_frame, width=30, show="*")
        canvas.create_window(500, 320, window=password)

        canvas.create_text(
            300, 368,
            text="Role",
            fill="white",
            font=("Segoe UI", 16, "bold")
        )
        
        roles = StringVar(value="Customer")
        rolesMenu = OptionMenu(self.signup_frame, roles, "Manager", "Customer")
        canvas.create_window(500, 370, window=rolesMenu)
        
        submitBtn = Button(
            self.signup_frame,
            text="Create Account",
            font=("Segoe UI", 12, "bold"),
            bg="#2cac2c",
            fg="white",
            activebackground="#222",
            bd=0,
            cursor="hand2",
            command=lambda: self.Signup(name.get(),username.get(),password.get(),roles.get())
        )
        canvas.create_window(400, 500, window=submitBtn)

        self.signup_frame.tkraise()

    
    def Run(self):
        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.resizable(False,False)
    
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.signin_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.signup_frame.place(relx=0.5, rely=0.5, anchor="center")  
        
        canvas = Canvas(self.main_frame, width=WIDTH, height=HEIGHT, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        
        canvas.create_text(
            410, 150,
            text="Snapp Food",
            fill="white",
            font=("Segoe UI", 40, "bold")
        )
        
        signupBtn = Button(
            self.main_frame,
            text="Sign Up",
            font=("Segoe UI", 18, "bold"),
            width=15,
            height=2,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            cursor="hand2",
            bd=0,
            command=lambda: self.signup_frame.tkraise()
        )

        signinBtn = Button(
            self.main_frame,
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
        
        canvas.create_window(250, 350, window=signupBtn)
        canvas.create_window(580, 350, window=signinBtn)
        
        self.CreateSignupFrame()
        self.main_frame.tkraise()
                
        self.root.mainloop()