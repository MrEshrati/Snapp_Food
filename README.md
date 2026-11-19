# Snapp Food

A desktop food-ordering coursework prototype built with Python, Tkinter, Pillow, and MongoDB. Customers can browse restaurants and menus, add items to a cart, and submit orders. Managers can manage restaurant menu items.

## Run locally

1. Install Python with Tkinter support and start MongoDB on `localhost:27017`.
2. Install the Python dependencies with `python -m pip install Pillow pymongo`.
3. Run `python main.py` from the repository root.

The app uses a local `Snapp_Food` database. The [original Persian notes](README.txt) describe optional sample data and the current sign-in workflow. Restart the app to switch users.

## Local accounts

New signups store a salted password hash. An existing account with a plaintext password is upgraded at its next successful sign-in.

To load the optional demo records in `main.py`, supply your own `SNAPP_DEMO_MANAGER_USERNAME`, `SNAPP_DEMO_MANAGER_PASSWORD`, `SNAPP_DEMO_CUSTOMER_USERNAME`, and `SNAPP_DEMO_CUSTOMER_PASSWORD` in the environment, then follow the original seeding notes. Uncomment the imports at the top of `main.py` for that one-time setup.
