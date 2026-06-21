from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.geometry("1200x700")
root.resizable(False, False)

# Background image
img = Image.open("./public/images/auth_section.jpg")
img = img.resize((1200, 700))
bg_img = ImageTk.PhotoImage(img)

canvas = Canvas(root, width=1200, height=700, highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_img, anchor="nw")

# Title
canvas.create_text(
    600, 120,
    text="Create Account",
    fill="white",
    font=("Segoe UI", 28, "bold")
)

# Username label + entry
canvas.create_text(
    450, 220,
    text="Username",
    fill="white",
    font=("Segoe UI", 14)
)

username_entry = Entry(root, width=30)
canvas.create_window(650, 220, window=username_entry)

# Name label + entry
canvas.create_text(
    450, 270,
    text="Name",
    fill="white",
    font=("Segoe UI", 14)
)

name_entry = Entry(root, width=30)
canvas.create_window(650, 270, window=name_entry)

# Password label + entry
canvas.create_text(
    450, 320,
    text="Password",
    fill="white",
    font=("Segoe UI", 14)
)

password_entry = Entry(root, width=30, show="*")
canvas.create_window(650, 320, window=password_entry)

# Role label
canvas.create_text(
    450, 370,
    text="Role",
    fill="white",
    font=("Segoe UI", 14)
)

canvas.create_text(
    450, 370,
    text="Role",
    fill="white",
    font=("Segoe UI", 14)
)

role_var = StringVar(value="Customer")
role_menu = OptionMenu(root, role_var, "Manager", "Customer")
canvas.create_window(650, 370, window=role_menu)

# Button
def signup():
    print(username_entry.get(), name_entry.get(), password_entry.get(), role_var.get())

button = Button(root, text="Sign Up", command=signup)
canvas.create_window(600, 450, window=button)

root.mainloop()