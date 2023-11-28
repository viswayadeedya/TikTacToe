import tkinter
import smtplib
import sqlite3
import re
from tkinter import messagebox
from random import randint

window = tkinter.Tk()
window.title("Login form")
window.geometry('405x550')
window.configure(bg='#333333')

# create reset_token globally
reset_token = 0


def check_mail(email_id):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.fullmatch(regex, email_id)


def reset_password():
    print(reset_token, forget_token_entry)
    if reset_token == int(forget_token_entry.get()):
        if len(forget_password_entry.get()) >= 5:
            conn = sqlite3.connect("user.db")
            table_create_query = '''CREATE TABLE IF NOT EXISTS user
                        (user_id INTEGER PRIMARY KEY, email_id TEXT, profile_name TEXT, password TEXT)
                        '''
            conn.execute(table_create_query)
            cursor = conn.cursor()
            cursor.execute(
                f'UPDATE user_details SET password = ? WHERE email_id = ?', (forget_password_entry.get(), forget_username_entry.get()))
            cursor.execute(f'SELECT password FROM user_details WHERE email_id = ?', (forget_username_entry.get(),))
            get_user = cursor.fetchall()
            print(get_user)
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo(title="Success",
                                message="Password has been successfully reset. Please Login to continue")
        else:
            messagebox.showinfo(title="Invalid password",
                                message="Password should have at least 5 characters")
    else:
        messagebox.showinfo(title="Invalid Token",
                            message="Please enter a valid token")


def register_user(email_id, profile_name, password):
    # CREATE DATABASE TABLE
    conn = sqlite3.connect("user.db")
    table_create_query = '''CREATE TABLE IF NOT EXISTS user
    (user_id INTEGER PRIMARY KEY, email_id TEXT, profile_name TEXT, password TEXT)
    '''
    conn.execute(table_create_query)
    cursor = conn.cursor()
    cursor.execute(f'SELECT email_id FROM user_details WHERE email_id = ?', (email_id,))
    get_user = cursor.fetchall()
    # Insert Data
    if len(get_user) == 0:
        data_insert_query = '''INSERT INTO user_details (email_id, profile_name, password) VALUES
            (?, ?, ?)'''
        data_insert_tuple = (email_id, profile_name, password)
        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        messagebox.showinfo(title="Registered Success", message="You successfully registered. Please Login to continue")
    else:
        messagebox.showinfo(title="User already exists", message="Try Login to continue")
    cursor.close()
    conn.close()


def generate_token():
    global reset_token
    if check_mail(forget_username_entry.get()):
        range_start = 10 ** (6 - 1)
        range_end = (10 ** 6) - 1
        reset_token = randint(range_start, range_end)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("viswayadeedya@gmail.com", "llhvaaomfmyledob")
        server.sendmail("viswayadeedya@gmail.com", forget_username_entry.get(),
                        str(reset_token) + " is your verification code for TicTacToe game.")
        print("mail sent")
    else:
        messagebox.showinfo(title="Invalid Email Id", message="Enter a valid email id.")


def login():
    # need to connect database
    conn = sqlite3.connect("user.db")
    table_create_query = '''CREATE TABLE IF NOT EXISTS user
        (user_id INTEGER PRIMARY KEY, email_id TEXT, profile_name TEXT, password TEXT)
        '''
    conn.execute(table_create_query)
    cursor = conn.cursor()
    cursor.execute(f'SELECT email_id, password FROM user_details WHERE email_id = ?', (username_entry.get(),))
    get_user = cursor.fetchall()
    # username = "test_user"
    password = "12345"
    # reset_password("viswayda@gmail.com")
    if len(get_user) != 0:
        if username_entry.get() in get_user[0] and password_entry.get() in get_user[0]:
            messagebox.showinfo(title="Login Success", message="You have successfully logged in.")
        else:
            messagebox.showerror(title="Invalid password", message="Forget Password? Please reset")
    else:
        messagebox.showerror(title="No User Found", message="Please Register to User")
    conn.close()


def register():
    # need to connect database
    username = "test_user"
    password = "12345"
    if len(register_username_entry.get()) >= 5 and len(register_profile_name_entry.get()) >= 3 and len(register_password_entry.get()) >= 5:
        register_user(register_username_entry.get(), register_profile_name_entry.get(), register_password_entry.get())
    else:
        messagebox.showerror(title="Error", message="Invalid register.")


def navigate(frame):
    frame.tkraise()


login_frame = tkinter.Frame(window, bg='#333333')
register_frame = tkinter.Frame(window, bg='#333333')
forget_frame = tkinter.Frame(window, bg='#333333')

login_frame.grid(row=0, column=1, sticky='news', padx=20)
register_frame.grid(row=0, column=1, sticky='nsew', padx=20)
forget_frame.grid(row=0, column=1, sticky='nsew', padx=20)

# Creating widgets
# Login frame
login_label = tkinter.Label(
    login_frame, text="TIC TAC TOE", bg='#333333', fg="#02952c", font=("Arial", 30))
username_label = tkinter.Label(
    login_frame, text="Email ID", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tkinter.Entry(login_frame, bg='#D3D3D3', font=("Arial", 16))
password_entry = tkinter.Entry(login_frame, bg='#D3D3D3', show="*", font=("Arial", 16))
password_label = tkinter.Label(
    login_frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = tkinter.Button(
    login_frame, text="Login", bg="#02952c", fg="#000", font=("Arial", 16), command=login)
forget_password_button = tkinter.Button(
    login_frame, text="Forget Password", bg='#333333', fg="#02952c", font=("Arial", 10),
    command=lambda: navigate(forget_frame))
register_button = tkinter.Button(
    login_frame, text="New User? Register here", bg='#333333', fg="#02952c", font=("Arial", 10),
    command=lambda: navigate(register_frame))

# Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=10)
forget_password_button.grid(row=4, column=0, columnspan=2, pady=20)
register_button.grid(row=5, column=0, columnspan=2, pady=0)
login_frame.tkraise()

# Register frame
register_label = tkinter.Label(
    register_frame, text="TIC TAC TOE", bg='#333333', fg="#02952c", font=("Arial", 30))
register_username_label = tkinter.Label(
    register_frame, text="Email ID", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
register_username_entry = tkinter.Entry(register_frame, bg='#D3D3D3', font=("Arial", 16))
register_profile_name_label = tkinter.Label(
    register_frame, text="Profile Name", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
register_profile_name_entry = tkinter.Entry(register_frame, bg='#D3D3D3', font=("Arial", 16))
register_password_entry = tkinter.Entry(register_frame, bg='#D3D3D3', show="*", font=("Arial", 16))
register_password_label = tkinter.Label(
    register_frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
register_button = tkinter.Button(
    register_frame, text="Register", bg="#02952c", fg="#000", font=("Arial", 16), command=register)
registered_button = tkinter.Button(
    register_frame, text="Already Registered? Login here", bg='#333333', fg="#02952c", font=("Arial", 10),
    command=lambda: navigate(login_frame))

# Placing widgets on the screen
register_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
register_username_label.grid(row=1, column=0)
register_username_entry.grid(row=1, column=1, pady=20)
register_profile_name_label.grid(row=2, column=0)
register_profile_name_entry.grid(row=2, column=1, pady=20)
register_password_label.grid(row=3, column=0)
register_password_entry.grid(row=3, column=1, pady=20)
register_button.grid(row=4, column=0, columnspan=2, pady=30)
registered_button.grid(row=5, column=0, columnspan=2, pady=0)

# Forget Password Frame
forget_label = tkinter.Label(
    forget_frame, text="TIC TAC TOE", bg='#333333', fg="#02952c", font=("Arial", 30))
forget_username_label = tkinter.Label(
    forget_frame, text="Email ID", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
forget_username_entry = tkinter.Entry(forget_frame, bg='#D3D3D3', font=("Arial", 16))
forget_token_label = tkinter.Label(
    forget_frame, text="Token", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
forget_token_entry = tkinter.Entry(forget_frame, bg='#D3D3D3', font=("Arial", 16))
forget_password_entry = tkinter.Entry(forget_frame, bg='#D3D3D3', show="*", font=("Arial", 16))
forget_password_label = tkinter.Label(
    forget_frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
token_button = tkinter.Button(
    forget_frame, text="Send Reset Token", bg='#333333', fg="#02952c", font=("Arial", 10),
    command=generate_token)
reset_button = tkinter.Button(
    forget_frame, text="Reset Password", bg="#02952c", fg="#000", font=("Arial", 16), command=reset_password)
registered_button = tkinter.Button(
    forget_frame, text="Already Registered? Login here", bg='#333333', fg="#02952c", font=("Arial", 10),
    command=lambda: navigate(login_frame))

# Placing widgets on the screen
forget_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
forget_username_label.grid(row=1, column=0)
forget_username_entry.grid(row=1, column=1, pady=20)
forget_token_label.grid(row=2, column=0)
forget_token_entry.grid(row=2, column=1, pady=20)
forget_password_label.grid(row=3, column=0)
forget_password_entry.grid(row=3, column=1, pady=20)
token_button.grid(row=4, column=0, columnspan=2, pady=10)
reset_button.grid(row=5, column=0, columnspan=2, pady=20)
registered_button.grid(row=6, column=0, columnspan=2, pady=0)

window.mainloop()
