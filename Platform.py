from db import DB
from User import User
from Manager import Manager
from Restaurant import Restaurant
from Customer import Customer
from Order import Order
from tkinter import *  # ignore
from tkinter import ttk, Canvas
from PIL import Image, ImageTk
import os
from constants import WIDTH, HEIGHT


class Platform:
    def __init__(self):
        self.db = DB()
        self.root = Tk()
        self.restaurants = []
        self.users = self.db.GetData("Users", "")
        self.current_user = []

        img = Image.open(os.path.join(".", "public", "images", "auth_section.png"))
        img = img.resize((WIDTH, HEIGHT))
        self.bg_img = ImageTk.PhotoImage(img)
        bgLabel = Label(self.root, image=self.bg_img)
        bgLabel.pack()

        self.main_frame = Frame(bgLabel)
        self.signin_frame = Frame(bgLabel)
        self.signup_frame = Frame(bgLabel)
        self.home_frame = Frame(bgLabel)
        self.menu_frame = Frame(bgLabel)
        self.addItem_frame = Frame(bgLabel)
        self.editItem_frame = Frame(bgLabel)
        self.cart_frame = Frame(bgLabel)
        self.order_frame = Frame(bgLabel)

    def Signup(self, name, username, password, role, alertText, canvas, restaurantName):

        user = User(name.get(), username.get(), password.get())
        validation = True
        if user.checkName():
            if user.checkUsername(self.users):
                if user.checkPassword():
                    user.createId(role.get(), self.users)
                else:
                    validation = False
                    canvas.itemconfig(
                        alertText,
                        text="Password is not valid(must be 8 or more characters)",
                    )
            else:
                validation = False
                canvas.itemconfig(
                    alertText,
                    text="Username is not valid(must be 5 or more letters and unique)",
                )
        else:
            validation = False
            canvas.itemconfig(
                alertText, text="Name is not valid(must be 5 or more letters)"
            )

        if role.get() == "Manager" and restaurantName.get() == "":
            validation = False
            canvas.itemconfig(alertText, text="Restaurant's name can not be empty")

        if validation:
            if role.get() == "Manager":
                self.db.PostData(
                    "Restaurants",
                    {"name": restaurantName.get(), "managerId": user._id, "orders": []},
                )

            self.db.PostData(
                "Users",
                {
                    "_id": user._id,
                    "name": user.name,
                    "username": user.username,
                    "password": user.password,
                },
            )

            name.delete(0, END)
            username.delete(0, END)
            password.delete(0, END)
            canvas.itemconfig(alertText, text="")
            restaurantName.delete(0, END)

            self.users = self.db.GetData("Users", "")
            self.main_frame.tkraise()

    def Signin(self, username, password, alertText, canvas):
        for user in self.users:
            if (
                user["username"] == username.get()
                and user["password"] == password.get()
            ):
                self.current_user = user
                username.delete(0, END)
                password.delete(0, END)
                canvas.itemconfig(alertText, text="")

                if self.current_user["_id"][0] == "m":
                    self.restaurants = self.db.GetData(
                        "Restaurants", {"managerId": self.current_user["_id"]}
                    )
                else:
                    self.restaurants = self.db.GetData("Restaurants", "")

                self.CreateHome()
                self.home_frame.tkraise()

                return

        canvas.itemconfig(alertText, text="Username/Password is Incorrectl")

    def submitOrder(self, res):
        restaurant = Restaurant(res["name"], res["managerId"])
        customer = Customer(self.current_user["_id"])
        order = customer.submitCart(self.current_user)
        restaurant.newOrder(order, res["_id"])
        self.openOrder(res)

    def addCart(self, item, restaurant):
        customer = Customer(self.current_user["_id"])
        customer.addToCart(item)
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        for widget in self.addItem_frame.winfo_children():
            widget.destroy()
        self.CreateMenu(restaurant)
        self.menu_frame.tkraise()

    def deleteCart(self, item, restaurant, page):
        customer = Customer(self.current_user["_id"])
        customer.removeFromCart(item)
        if page == "cart":
            for widget in self.cart_frame.winfo_children():
                widget.destroy()
            self.createCart(restaurant)
            self.cart_frame.tkraise()
        else:
            for widget in self.menu_frame.winfo_children():
                widget.destroy()
            for widget in self.addItem_frame.winfo_children():
                widget.destroy()
            self.CreateMenu(restaurant)
            self.menu_frame.tkraise()

    def addItem(self, name, price, types, available, alertText, canvas):
        validation = True
        if name.get() == "" or len(name.get()) < 5:
            validation = False
            canvas.itemconfig(
                alertText, text="Name is not valid(must be 5 or more letters)"
            )
        elif price.get() == "":
            validation = False
            canvas.itemconfig(alertText, text="Price must not be empty")

        if validation:
            restaurant = self.db.GetData(
                "Restaurants", {"managerId": self.current_user["_id"]}
            )
            manager = Manager(restaurant[0]["_id"])
            manager.addItem(name.get(), price.get(), available.get(), types.get())
            name.delete(0, END)
            price.delete(0, END)
            canvas.itemconfig(alertText, text="")

            for widget in self.menu_frame.winfo_children():
                widget.destroy()
            for widget in self.addItem_frame.winfo_children():
                widget.destroy()
            self.CreateMenu(restaurant[0])
            self.menu_frame.tkraise()

    def editItem(self, item, name, price, types, available, alertText, canvas):
        validation = True
        if name.get() == "" or len(name.get()) < 5:
            validation = False
            canvas.itemconfig(
                alertText, text="Name is not valid(must be 5 or more letters)"
            )
        elif price.get() == "":
            validation = False
            canvas.itemconfig(alertText, text="Price must not be empty")

        if validation:
            restaurant = self.db.GetData(
                "Restaurants", {"managerId": self.current_user["_id"]}
            )
            manager = Manager(restaurant[0]["_id"])
            manager.editItem(
                name.get(), price.get(), available.get(), types.get(), item["_id"]
            )
            name.delete(0, END)
            price.delete(0, END)
            canvas.itemconfig(alertText, text="")

            for widget in self.menu_frame.winfo_children():
                widget.destroy()
            for widget in self.addItem_frame.winfo_children():
                widget.destroy()

            self.CreateMenu(restaurant[0])
            self.menu_frame.tkraise()

    def deleteItem(self, manager, item, res):
        manager.deleteItem(item["_id"])

        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        for widget in self.addItem_frame.winfo_children():
            widget.destroy()
        self.CreateMenu(res)
        self.menu_frame.tkraise()

    def CreateHome(self):

        mainFrame = Frame(self.home_frame)
        mainFrame.pack(fill="both", expand=True)

        canvas = Canvas(mainFrame, width=WIDTH - 250, height=HEIGHT, bg="#1e1e1e")
        scrollbar = ttk.Scrollbar(mainFrame, orient="vertical", command=canvas.yview)

        cards_frame = Frame(canvas, padx=10, pady=10, bg="#1e1e1e")

        cards_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=cards_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        for res in self.restaurants:
            card = Frame(
                cards_frame,
                height=150,
                width=300,
                bd=1,
                relief="solid",
                padx=15,
                pady=15,
            )

            card.pack(fill="x", padx=20, pady=10)

            card.pack_propagate(False)

            Label(card, text=res["name"], font=("Segoe UI", 16, "bold")).pack(
                anchor="w"
            )

            Label(
                card,
                text=f"Manager:  {(self.db.GetData('Users', {'_id': res['managerId']}))[0]['name']}",
                font=("Segoe UI", 11),
            ).pack(anchor="w")

            Button(
                card,
                text="View Menu",
                font=("Segoe UI", 9, "bold"),
                width=9,
                height=2,
                bg="#222",
                fg="white",
                bd=0,
                cursor="hand2",
                command=lambda r=res: self.OpenMenu(r),
            ).pack(anchor="se")

        right_frame = Frame(mainFrame, width=250, bg="#f0f0f0")
        right_frame.pack(side="right", fill="y")
        right_frame.pack_propagate(False)

        Label(
            right_frame,
            text="Current User",
            font=("Segoe UI", 16, "bold"),
            bg="#f0f0f0",
        ).pack(pady=(20, 10))

        Label(
            right_frame,
            text=self.current_user["name"],
            font=("Segoe UI", 12),
            bg="#f0f0f0",
        ).pack()

        role = "Manager" if self.current_user["_id"][0] == "m" else "Customer"
        Label(right_frame, text=role, font=("Segoe UI", 12), bg="#f0f0f0").pack()

        if self.current_user["_id"][0] == "c":
            cart_btn = Button(
                right_frame,
                text="🛒 Cart",
                font=("Segoe UI", 14, "bold"),
                width=15,
                height=2,
                bg="#2cac2c",
                fg="white",
                bd=0,
                cursor="hand2",
                command=lambda: self.openCart(res),
            )
            cart_btn.pack(pady=(40, 15))

            orders_btn = Button(
                right_frame,
                text="📦 Orders",
                font=("Segoe UI", 14, "bold"),
                width=15,
                height=2,
                bg="#2196F3",
                fg="white",
                bd=0,
                cursor="hand2",
                command=lambda: self.openOrder(res),
            )

            orders_btn.pack(pady=15)

    def OpenMenu(self, restaurant):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        for widget in self.addItem_frame.winfo_children():
            widget.destroy()
        self.CreateMenu(restaurant)
        self.menu_frame.tkraise()

    def openEditItem(self, item):
        for widget in self.editItem_frame.winfo_children():
            widget.destroy()
        self.CreateEditItem(item)
        self.editItem_frame.tkraise()

    def openCart(self, res):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()
        self.createCart(res)
        self.cart_frame.tkraise()

    def openOrder(self, res):
        for widget in self.order_frame.winfo_children():
            widget.destroy()
        self.createOrder(res)
        self.order_frame.tkraise()

    def createOrder(self, res):

        mainFrame = Frame(self.order_frame)
        mainFrame.pack(fill="both", expand=True)

        canvas = Canvas(mainFrame, width=WIDTH - 250, height=HEIGHT, bg="#1e1e1e")
        scrollbar = ttk.Scrollbar(mainFrame, orient="vertical", command=canvas.yview)

        cards_frame = Frame(canvas, padx=10, pady=10, bg="#1e1e1e")

        cards_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=cards_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        customer = Customer(self.current_user["_id"])
        orders = customer.showOrders(self.current_user)
        if self.current_user["_id"][0] == "m":
            restaurant = Restaurant(res["name"], res["managerId"])
            orders = restaurant.Orders(res["_id"])

        for order in orders:
            card = Frame(cards_frame, width=500, bd=1, relief="solid", padx=15, pady=10)

            card.pack(fill="x", padx=20, pady=10)

            Label(
                card, text=f"OrderId: {order['_id']}", font=("Segoe UI", 16, "bold")
            ).pack(anchor="w")

            Label(
                card,
                text=f"Customer: {order['customer']['name']}",
                font=("Segoe UI", 11),
            ).pack(anchor="w")

            Label(
                card,
                text="-------------------------------------------------------------------",
                font=("Segoe UI", 11),
            ).pack(anchor="w")

            for item in order["items"][0]["items"]:
                Label(
                    card, text=f"name: {item['name']}", font=("Segoe UI", 16, "bold")
                ).pack(anchor="w")

                Label(card, text=f"price: {item['price']}", font=("Segoe UI", 11)).pack(
                    anchor="w"
                )

                Label(
                    card, text=f"Type: {item['itemType']}", font=("Segoe UI", 11)
                ).pack(anchor="w")

                restaurantName = (
                    self.db.GetData("Restaurants", {"_id": item["restaurantId"]})
                )[0]["name"]
                Label(
                    card, text=f"Restaurant: {restaurantName}", font=("Segoe UI", 11)
                ).pack(anchor="w")

                Label(
                    card,
                    text="-------------------------------------------------------------------",
                    font=("Segoe UI", 11),
                ).pack(anchor="w")

            buttons_frame = Frame(card)
            buttons_frame.pack(anchor="e", pady=5)

            Label(
                buttons_frame,
                text=f"Total Price: {order['totalPrice']}",
                font=("Segoe UI", 11),
            ).pack(side="left", padx=5)

        right_frame = Frame(mainFrame, width=250, bg="#f0f0f0")

        right_frame.pack(side="right", fill="y")
        right_frame.pack_propagate(False)

        Label(
            right_frame,
            text="Current User",
            font=("Segoe UI", 16, "bold"),
            bg="#f0f0f0",
        ).pack(pady=(20, 10))

        Label(
            right_frame,
            text=self.current_user["name"],
            font=("Segoe UI", 12),
            bg="#f0f0f0",
        ).pack()

        role = "Manager" if self.current_user["_id"][0] == "m" else "Customer"
        Label(right_frame, text=role, font=("Segoe UI", 12), bg="#f0f0f0").pack()

        backBtn = Button(
            right_frame,
            text="← Back",
            font=("Segoe UI", 14, "bold"),
            width=15,
            height=2,
            bg="#222",
            fg="white",
            bd=0,
            cursor="hand2",
            command=lambda: self.home_frame.tkraise(),
        )
        backBtn.pack(pady=(40, 15), anchor="s")

    def createCart(self, res):

        mainFrame = Frame(self.cart_frame)
        mainFrame.pack(fill="both", expand=True)

        canvas = Canvas(mainFrame, width=WIDTH - 250, height=HEIGHT, bg="#1e1e1e")
        scrollbar = ttk.Scrollbar(mainFrame, orient="vertical", command=canvas.yview)

        cards_frame = Frame(canvas, padx=10, pady=10, bg="#1e1e1e")

        cards_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=cards_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        customer = Customer(self.current_user["_id"])
        if customer.cart != []:
            for item in customer.cart[0]["items"]:
                card = Frame(
                    cards_frame,
                    height=180,
                    width=300,
                    bd=1,
                    relief="solid",
                    padx=15,
                    pady=10,
                )

                card.pack(fill="x", padx=20, pady=10)

                card.pack_propagate(False)

                Label(card, text=item["name"], font=("Segoe UI", 16, "bold")).pack(
                    anchor="w"
                )

                Label(
                    card, text=f"Type: {item['itemType']}", font=("Segoe UI", 11)
                ).pack(anchor="w")

                restaurantName = (
                    self.db.GetData("Restaurants", {"_id": item["restaurantId"]})
                )[0]["name"]
                Label(
                    card, text=f"Restaurant: {restaurantName}", font=("Segoe UI", 11)
                ).pack(anchor="w")

                Label(card, text=f"{item['price']} Rial", font=("Segoe UI", 11)).pack(
                    anchor="e"
                )

                Button(
                    card,
                    text="     🗑️",
                    font=("Segoe UI", 12, "bold"),
                    width=3,
                    height=1,
                    bg="red",
                    fg="white",
                    bd=0,
                    cursor="hand2",
                    command=lambda i=item: self.deleteCart(i, res, "cart"),
                ).pack(side="right", padx=5)

        right_frame = Frame(mainFrame, width=250, bg="#f0f0f0")

        right_frame.pack(side="right", fill="y")
        right_frame.pack_propagate(False)

        Label(
            right_frame,
            text="Current User",
            font=("Segoe UI", 16, "bold"),
            bg="#f0f0f0",
        ).pack(pady=(20, 10))

        Label(
            right_frame,
            text=self.current_user["name"],
            font=("Segoe UI", 12),
            bg="#f0f0f0",
        ).pack()

        role = "Manager" if self.current_user["_id"][0] == "m" else "Customer"
        Label(right_frame, text=role, font=("Segoe UI", 12), bg="#f0f0f0").pack()

        if customer.cart != []:
            cart_btn = Button(
                right_frame,
                text="🛒 Submit Cart",
                font=("Segoe UI", 14, "bold"),
                width=15,
                height=2,
                bg="blue",
                fg="white",
                bd=0,
                cursor="hand2",
                command=lambda: self.submitOrder(res),
            )
            cart_btn.pack(pady=(40, 15))

        backBtn = Button(
            right_frame,
            text="← Back",
            font=("Segoe UI", 14, "bold"),
            width=15,
            height=2,
            bg="#222",
            fg="white",
            bd=0,
            cursor="hand2",
            command=lambda: self.home_frame.tkraise(),
        )
        backBtn.pack(pady=(40, 15), anchor="s")

    def CreateMenu(self, res):

        restaurant = Restaurant(res["name"], res["managerId"])
        restaurant.Menu(res["_id"])

        manager = Manager(res["_id"])

        mainFrame = Frame(self.menu_frame)
        mainFrame.pack(fill="both", expand=True)

        canvas = Canvas(mainFrame, width=WIDTH - 250, height=HEIGHT, bg="#1e1e1e")
        scrollbar = ttk.Scrollbar(mainFrame, orient="vertical", command=canvas.yview)

        cards_frame = Frame(canvas, padx=10, pady=10, bg="#1e1e1e")

        cards_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=cards_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        for item in restaurant.menu:
            card = Frame(
                cards_frame,
                height=180,
                width=300,
                bd=1,
                relief="solid",
                padx=15,
                pady=10,
            )

            card.pack(fill="x", padx=20, pady=10)

            card.pack_propagate(False)

            Label(card, text=item["name"], font=("Segoe UI", 16, "bold")).pack(
                anchor="w"
            )

            Label(card, text=f"Type: {item['itemType']}", font=("Segoe UI", 11)).pack(
                anchor="w"
            )

            Label(card, text=f"{item['price']} Rial", font=("Segoe UI", 11)).pack(
                anchor="e"
            )

            if self.current_user["_id"][0] == "c":
                inCart = False
                customer = Customer(self.current_user["_id"])
                if customer.cart != []:
                    for it in customer.cart[0]["items"]:
                        if (
                            it["name"] == item["name"]
                            and it["restaurantId"] == item["restaurantId"]
                        ):
                            Label(
                                card, text="In Cart", font=("Segoe UI", 11), fg="green"
                            ).pack(anchor="e")
                            Button(
                                card,
                                text="     🗑️",
                                font=("Segoe UI", 12, "bold"),
                                width=3,
                                height=1,
                                bg="red",
                                fg="white",
                                bd=0,
                                cursor="hand2",
                                command=lambda i=item: self.deleteCart(i, res, ""),
                            ).pack(side="left", padx=5)
                            inCart = True

                if inCart == False:
                    if item["isAvailable"] == "Available":
                        Button(
                            card,
                            text="addToCart",
                            font=("Segoe UI", 8, "bold"),
                            width=8,
                            height=2,
                            bg="#222",
                            fg="white",
                            bd=0,
                            cursor="hand2",
                            command=lambda i=item: self.addCart(i, res),
                        ).pack(anchor="e")

                    else:
                        Label(
                            card, text="Not Available", font=("Segoe UI", 11), fg="red"
                        ).pack(anchor="e")
            else:
                Label(
                    card, text=item["isAvailable"], font=("Segoe UI", 11), fg="blue"
                ).pack(anchor="w")

                buttons_frame = Frame(card)
                buttons_frame.pack(anchor="e", pady=5)

                Button(
                    buttons_frame,
                    text="     🗑️",
                    font=("Segoe UI", 12, "bold"),
                    width=3,
                    height=1,
                    bg="red",
                    fg="white",
                    bd=0,
                    cursor="hand2",
                    command=lambda i=item: self.deleteItem(manager, i, res),
                ).pack(side="left", padx=5)

                Button(
                    buttons_frame,
                    text="📝",
                    font=("Segoe UI", 12, "bold"),
                    width=3,
                    height=1,
                    bg="#2196F3",
                    fg="white",
                    bd=0,
                    cursor="hand2",
                    command=lambda i=item: self.openEditItem(i),
                ).pack(side="left", padx=5)

        right_frame = Frame(mainFrame, width=250, bg="#f0f0f0")
        right_frame.pack(side="right", fill="y")
        right_frame.pack_propagate(False)

        Label(
            right_frame,
            text="Current User",
            font=("Segoe UI", 16, "bold"),
            bg="#f0f0f0",
        ).pack(pady=(20, 10))

        Label(
            right_frame,
            text=self.current_user["name"],
            font=("Segoe UI", 12),
            bg="#f0f0f0",
        ).pack()

        role = "Manager" if self.current_user["_id"][0] == "m" else "Customer"
        Label(right_frame, text=role, font=("Segoe UI", 12), bg="#f0f0f0").pack()

        if self.current_user["_id"][0] == "m":
            ItemAddBtn = Button(
                right_frame,
                text="Add Item",
                font=("Segoe UI", 14, "bold"),
                width=15,
                height=2,
                bg="#2cac2c",
                fg="white",
                bd=0,
                cursor="hand2",
                command=lambda: self.addItem_frame.tkraise(),
            )
            ItemAddBtn.pack(pady=(40, 15))
            self.CreateAddItem()

            orders_btn = Button(
                right_frame,
                text="📦 Orders",
                font=("Segoe UI", 14, "bold"),
                width=15,
                height=2,
                bg="#2196F3",
                fg="white",
                bd=0,
                cursor="hand2",
                command=lambda: self.openOrder(res),
            )

            orders_btn.pack(pady=15)

        backBtn = Button(
            right_frame,
            text="← Back",
            font=("Segoe UI", 14, "bold"),
            width=15,
            height=2,
            bg="#222",
            fg="white",
            bd=0,
            cursor="hand2",
            command=lambda: self.home_frame.tkraise(),
        )
        backBtn.pack(pady=(40, 15), anchor="s")

    def CreateAddItem(self):
        canvas = Canvas(
            self.addItem_frame, width=WIDTH, height=HEIGHT, highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        backBtn = Button(
            self.addItem_frame,
            text="← Back",
            font=("Segoe UI", 12, "bold"),
            bg="#555555",
            fg="white",
            activebackground="#444444",
            bd=0,
            cursor="hand2",
            command=lambda: self.menu_frame.tkraise(),
        )
        canvas.create_window(50, 50, window=backBtn)

        canvas.create_text(
            420,
            115,
            text="Add Item",
            fill="#2cac2c",
            font=("Segoe", 32, "bold"),
        )

        canvas.create_text(
            300, 215, text="Name", fill="white", font=("Segoe UI", 16, "bold")
        )

        name = Entry(self.addItem_frame, width=30)
        canvas.create_window(500, 220, window=name)

        canvas.create_text(
            300, 265, text="Price", fill="white", font=("Segoe UI", 16, "bold")
        )

        price = Entry(self.addItem_frame, width=30)
        canvas.create_window(500, 270, window=price)

        canvas.create_text(
            300, 340, text="Item Type", fill="white", font=("Segoe UI", 16, "bold")
        )

        itemTypes = StringVar(value="Food")
        typesMenu = OptionMenu(self.addItem_frame, itemTypes, "Food", "Drink")
        canvas.create_window(500, 343, window=typesMenu)

        canvas.create_text(
            300, 390, text="Availability", fill="white", font=("Segoe UI", 16, "bold")
        )

        Availability = StringVar(value="Available")
        availabilityMenu = OptionMenu(
            self.addItem_frame, Availability, "Available", "NotAvailable"
        )
        canvas.create_window(500, 393, window=availabilityMenu)

        alertText = canvas.create_text(
            420,
            430,
            text="",
            fill="red",
            font=("Segoe", 12, "bold"),
        )

        submitBtn = Button(
            self.addItem_frame,
            text="Add Item",
            font=("Segoe UI", 12, "bold"),
            bg="#2cac2c",
            fg="white",
            activebackground="#222",
            bd=0,
            cursor="hand2",
            command=lambda: self.addItem(
                name, price, itemTypes, Availability, alertText, canvas
            ),
        )
        canvas.create_window(400, 500, window=submitBtn)

    def CreateEditItem(self, item):
        canvas = Canvas(
            self.editItem_frame, width=WIDTH, height=HEIGHT, highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        backBtn = Button(
            self.editItem_frame,
            text="← Back",
            font=("Segoe UI", 12, "bold"),
            bg="#555555",
            fg="white",
            activebackground="#444444",
            bd=0,
            cursor="hand2",
            command=lambda: self.menu_frame.tkraise(),
        )
        canvas.create_window(50, 50, window=backBtn)

        canvas.create_text(
            420,
            115,
            text="Add Item",
            fill="#2cac2c",
            font=("Segoe", 32, "bold"),
        )

        canvas.create_text(
            300, 215, text="Name", fill="white", font=("Segoe UI", 16, "bold")
        )

        name = Entry(self.editItem_frame, width=30)
        name.insert(0, item["name"])
        canvas.create_window(500, 220, window=name)

        canvas.create_text(
            300, 265, text="Price", fill="white", font=("Segoe UI", 16, "bold")
        )

        price = Entry(self.editItem_frame, width=30)
        price.insert(0, item["price"])
        canvas.create_window(500, 270, window=price)

        canvas.create_text(
            300, 340, text="Item Type", fill="white", font=("Segoe UI", 16, "bold")
        )

        itemTypes = StringVar(value=item["itemType"])
        typesMenu = OptionMenu(self.editItem_frame, itemTypes, "Food", "Drink")
        canvas.create_window(500, 343, window=typesMenu)

        canvas.create_text(
            300, 390, text="Availability", fill="white", font=("Segoe UI", 16, "bold")
        )

        Availability = StringVar(value=item["isAvailable"])
        availabilityMenu = OptionMenu(
            self.editItem_frame, Availability, "Available", "NotAvailable"
        )
        canvas.create_window(500, 393, window=availabilityMenu)

        alertText = canvas.create_text(
            420,
            430,
            text="",
            fill="red",
            font=("Segoe", 12, "bold"),
        )

        submitBtn = Button(
            self.editItem_frame,
            text="Add Item",
            font=("Segoe UI", 12, "bold"),
            bg="#2cac2c",
            fg="white",
            activebackground="#222",
            bd=0,
            cursor="hand2",
            command=lambda: self.editItem(
                item, name, price, itemTypes, Availability, alertText, canvas
            ),
        )
        canvas.create_window(400, 500, window=submitBtn)

    def CreateSigninFrame(self):
        canvas = Canvas(
            self.signin_frame, width=WIDTH, height=HEIGHT, highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        backBtn = Button(
            self.signin_frame,
            text="← Back",
            font=("Segoe UI", 12, "bold"),
            bg="#555555",
            fg="white",
            activebackground="#444444",
            bd=0,
            cursor="hand2",
            command=lambda: self.main_frame.tkraise(),
        )
        canvas.create_window(50, 50, window=backBtn)

        canvas.create_text(
            400,
            115,
            text="Sign In",
            fill="#2cac2c",
            font=("Segoe", 32, "bold"),
        )

        canvas.create_text(
            300, 265, text="Username", fill="white", font=("Segoe UI", 16, "bold")
        )

        username = Entry(self.signin_frame, width=30)
        canvas.create_window(500, 270, window=username)

        canvas.create_text(
            300, 315, text="Password", fill="white", font=("Segoe UI", 16, "bold")
        )

        password = Entry(self.signin_frame, width=30, show="*")
        canvas.create_window(500, 320, window=password)

        alertText = canvas.create_text(
            420,
            440,
            text="",
            fill="red",
            font=("Segoe", 12, "bold"),
        )

        submitBtn = Button(
            self.signin_frame,
            text="Sign In",
            font=("Segoe UI", 12, "bold"),
            bg="#2cac2c",
            fg="white",
            activebackground="#222",
            bd=0,
            cursor="hand2",
            command=lambda: self.Signin(username, password, alertText, canvas),
        )
        canvas.create_window(400, 500, window=submitBtn)

    def CreateSignupFrame(self):
        canvas = Canvas(
            self.signup_frame, width=WIDTH, height=HEIGHT, highlightthickness=0
        )
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
            command=lambda: self.main_frame.tkraise(),
        )
        canvas.create_window(50, 50, window=backBtn)

        canvas.create_text(
            420,
            115,
            text="Create Account",
            fill="#2cac2c",
            font=("Segoe", 32, "bold"),
        )

        canvas.create_text(
            300, 215, text="Name", fill="white", font=("Segoe UI", 16, "bold")
        )

        name = Entry(self.signup_frame, width=30)
        canvas.create_window(500, 220, window=name)

        canvas.create_text(
            300, 265, text="Username", fill="white", font=("Segoe UI", 16, "bold")
        )

        username = Entry(self.signup_frame, width=30)
        canvas.create_window(500, 270, window=username)

        canvas.create_text(
            300, 315, text="Password", fill="white", font=("Segoe UI", 16, "bold")
        )

        password = Entry(self.signup_frame, width=30, show="*")
        canvas.create_window(500, 320, window=password)

        canvas.create_text(
            300, 368, text="Role", fill="white", font=("Segoe UI", 16, "bold")
        )

        roles = StringVar(value="Customer")
        rolesMenu = OptionMenu(self.signup_frame, roles, "Manager", "Customer")
        canvas.create_window(500, 370, window=rolesMenu)

        canvas.create_text(
            250,
            412,
            text="Restaurant Name(for managers only)",
            fill="white",
            font=("Segoe UI", 16, "bold"),
        )

        restaurantName = Entry(
            self.signup_frame,
            width=30,
        )
        canvas.create_window(550, 415, window=restaurantName)

        alertText = canvas.create_text(
            420,
            460,
            text="",
            fill="red",
            font=("Segoe", 12, "bold"),
        )

        submitBtn = Button(
            self.signup_frame,
            text="Create Account",
            font=("Segoe UI", 12, "bold"),
            bg="#2cac2c",
            fg="white",
            activebackground="#222",
            bd=0,
            cursor="hand2",
            command=lambda: self.Signup(
                name, username, password, roles, alertText, canvas, restaurantName
            ),
        )
        canvas.create_window(400, 500, window=submitBtn)

    def Run(self):
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.signin_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.signup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.home_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.addItem_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.editItem_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.cart_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.order_frame.place(relx=0.5, rely=0.5, anchor="center")

        canvas = Canvas(
            self.main_frame, width=WIDTH, height=HEIGHT, highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        canvas.create_text(
            410, 150, text="Snapp Food", fill="white", font=("Segoe UI", 40, "bold")
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
            command=lambda: self.signup_frame.tkraise(),
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
            command=lambda: self.signin_frame.tkraise(),
        )

        canvas.create_window(250, 350, window=signupBtn)
        canvas.create_window(580, 350, window=signinBtn)

        self.CreateSignupFrame()
        self.CreateSigninFrame()

        self.main_frame.tkraise()

        self.root.mainloop()
