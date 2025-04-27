from tkinter import *
from tkinter import messagebox
import pandas as pd
from subprocess import call
import pymysql


def Login_data(username, password):
    global status
    global mycursor
    global con
    username_data = username.get()
    password_data = password.get()
    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()

    except FileNotFoundError:
        messagebox.showerror("ERROR", "Connection Lost!!")

    query = "use users"
    mycursor.execute(query)
    query2 = "SELECT * FROM userdata where username=%s and userpassword=%s"
    mycursor.execute(query2, (username_data, password_data))
    row = mycursor.fetchone()
    if row==None:
        messagebox.showerror("ERROR", "Invalid Username or Password")
    else:
        query3 = "UPDATE userdata SET login_status = 1 where username = %s"
        mycursor.execute(query3, (username_data))
        con.commit()

        if username_data == "admin":
            adminpage()

        else:
            Homepage()




def sign_in(username, password, Email):
    username_data = username.get()
    password_data = password.get()
    Email_data = Email.get()
    subs = 0
    log = 0
    UserID = "null"
    global con
    global mycursor2
    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor2 = con.cursor()

    except FileNotFoundError:
        messagebox.showerror("ERROR", "Connection Lost!!")

    try:
        query = "use users"
        mycursor2.execute(query)
        query2 = """INSERT INTO userdata (username, userpassword, Email, subscribe, login_status) VALUES (%s, %s, %s, %s, %s)"""
        mycursor2.execute(query2,(username_data, password_data, Email_data, subs, log))
        con.commit()
        con.close()
        messagebox.showinfo("yes done", "done!!")

    except FileNotFoundError:
            messagebox.showerror("ERROR", "Enter all Info")



def on_enter(e):
    username.delete(0, "end")

def on_leave(e):
    name = username.get()
    if name == '':
        username.insert(0, "Username")

def on_enter2(e):
    Password.delete(0, "end")

def on_leave2(e):
    name = Password.get()
    if name == '':
        Password.insert(0, "Password")

def on_enter3(e):
    signin_username.delete(0, "end")

def on_leave3(e):
    name = signin_username.get()
    if name == '':
        signin_username.insert(0, "Username")

def on_enter4(e):
    signin_password.delete(0, "end")

def on_leave4(e):
    name = signin_password.get()
    if name == '':
        signin_password.insert(0, "Password")

def on_enter5(e):
    Passwordl.delete(0, "end")

def on_leave5(e):
    name = Passwordl.get()
    if name == '':
        Passwordl.insert(0, "Password")

def on_enter6(e):
    signin_Email.delete(0, "end")

def on_leave6(e):
    name = signin_Email.get()
    if name == '':
        signin_Email.insert(0, "Email")

def hide():
    eyeopen_img.config(file="Assets/closeeye.png")
    Password.config(show="*")
    eyeopen_btn.config(command=show)

def show():
    eyeopen_img.config(file="Assets/openeye.png")
    Password.config(show="")
    eyeopen_btn.config(command=hide)

def hide2():
    eyeopen_img2.config(file="Assets/closeeye.png")
    Passwordl.config(show="*")
    eyeopen_btn2.config(command=show2)

def show2():
    eyeopen_img2.config(file="Assets/openeye.png")
    Passwordl.config(show="")
    eyeopen_btn2.config(command=hide2)

def hide3():
    eyeopen_img3.config(file="Assets/closeeye.png")
    signin_password.config(show="*")
    eyeopen_btn3.config(command=show3)

def show3():
    eyeopen_img3.config(file="Assets/openeye.png")
    signin_password.config(show="")
    eyeopen_btn3.config(command=hide3)


def login():
    global intro_root
    global eyeopen_btn
    global eyeopen_img
    global username
    global Password
    global frame_login
    intro_root = Tk()
    intro_root.title("Login Page")
    intro_root.geometry("1000x600+150+10")
    intro_root.resizable(False, False)
    intro_root.config(bg="#CEE6F3")

    login_img = PhotoImage(file="Assets//book.png")
    login = Label(intro_root, image=login_img, bg="#CEE6F3")
    login.place(x=-25, y=50)

    frame_login = Frame(intro_root, width=535, height=500, bg="white")
    frame_login.place(x=450, y=50)

    login_text = Label(frame_login, text="Login", font=("Microsoft YaHei UI Light", 50), bg="white", fg="#19A7CE")
    login_text.place(x=190, y=40)

    username = Entry(frame_login, fg="black", font=("Microsoft YaHei UI Light", 20), width=25, bg="white", border=0)
    username.place(x=100, y=180)
    username.insert(0, "Username")
    username.bind("<FocusIn>", on_enter)
    username.bind("<FocusOut>", on_leave)

    line1 = Frame(frame_login, width=375, height=2, bg="black")
    line1.place(x=90, y=220)

    Password = Entry(frame_login, fg="black", font=("Microsoft YaHei UI Light", 20), width=25, bg="white", border=0)
    Password.place(x=100, y=270)
    Password.insert(0, "Password")
    Password.bind("<FocusIn>", on_enter2)
    Password.bind("<FocusOut>", on_leave2)

    eyeopen_img = PhotoImage(file="Assets/openeye.png")
    eyeopen_btn = Button(frame_login, image=eyeopen_img, bg="white", border=0, activebackground="white", command=hide)
    eyeopen_btn.place(x=430, y=270)

    line2 = Frame(frame_login, width=375, height=2, bg="black")
    line2.place(x=90, y=310)

    login_btn = Button(frame_login, text="Login", font=("Roboto", 20), padx=145, fg="white", bg="#19A7CE",command=lambda:Login_data(username, Password), cursor="hand2")
    login_btn.place(x=87, y=370)

    signin = Label(frame_login, text="Not Registered?", font=("Microsoft YaHei UI Light", 11), bg="white")
    signin.place(x=150, y=450)

    signin_btn = Button(frame_login, text="Create an Account", font=("Microsoft YaHei UI Light", 11), bg="white", border=0, fg="#19A7CE", cursor="hand2", command=signup)
    signin_btn.place(x=260, y=448)

    intro_root.mainloop()


def login_frame():
    global username
    global Passwordl
    global eyeopen_img2
    global eyeopen_btn2
    signin_frame.destroy()
    frame_login = Frame(intro_root, width=535, height=500, bg="white")
    frame_login.place(x=450, y=50)

    login_text = Label(frame_login, text="Login", font=("Microsoft YaHei UI Light", 50), bg="white", fg="#19A7CE")
    login_text.place(x=190, y=40)

    username = Entry(frame_login, fg="black", font=("Microsoft YaHei UI Light", 20), width=25, bg="white", border=0)
    username.place(x=100, y=180)
    username.insert(0, "Username")
    username.bind("<FocusIn>", on_enter)
    username.bind("<FocusOut>", on_leave)

    line1 = Frame(frame_login, width=375, height=2, bg="black")
    line1.place(x=90, y=220)

    Passwordl = Entry(frame_login, fg="black", font=("Microsoft YaHei UI Light", 20), width=25, bg="white", border=0)
    Passwordl.place(x=100, y=270)
    Passwordl.insert(0, "Password")
    Passwordl.bind("<FocusIn>", on_enter5)
    Passwordl.bind("<FocusOut>", on_leave5)


    eyeopen_img2 = PhotoImage(file="Assets/openeye.png")
    eyeopen_btn2 = Button(frame_login, image=eyeopen_img2, bg="white", border=0, activebackground="white", command=hide2)
    eyeopen_btn2.place(x=430, y=270)

    line2 = Frame(frame_login, width=375, height=2, bg="black")
    line2.place(x=90, y=310)

    login_btn = Button(frame_login, text="Login", font=("Roboto", 20), padx=145, fg="white", bg="#19A7CE",
                       command=lambda:Login_data(username, Passwordl), cursor="hand2")
    login_btn.place(x=87, y=370)

    signin = Label(frame_login, text="Not Registered?", font=("Microsoft YaHei UI Light", 11), bg="white")
    signin.place(x=150, y=450)

    signin_btn = Button(frame_login, text="Create an Account", font=("Microsoft YaHei UI Light", 11), bg="white",
                        border=0, fg="#19A7CE", cursor="hand2", command=signup)
    signin_btn.place(x=260, y=448)


def signup():
    global signin_username
    global signin_password
    global eyeopen_img3
    global eyeopen_btn3
    global signin_frame
    global signin_Email
    frame_login.destroy()

    signin_frame = Frame(intro_root, width=535, height=500, bg="white")
    signin_frame.place(x=450, y=50)

    signin_text = Label(signin_frame, text="SignIn", font=("Microsoft YaHei UI Light", 40), bg="white", fg="#19A7CE")
    signin_text.place(x=190, y=10)

    signin_Email= Entry(signin_frame, fg="black", font=("Microsoft YaHei UI Light", 20), width=25, bg="white", border=0)
    signin_Email.place(x=100, y=120)
    signin_Email.insert(0, "Email")
    signin_Email.bind("<FocusIn>", on_enter6)
    signin_Email.bind("<FocusOut>", on_leave6)

    line3 = Frame(signin_frame, width=375, height=2, bg="black")
    line3.place(x=90, y=160)

    signin_username = Entry(signin_frame, fg="black", font=("Microsoft YaHei UI Light", 20), width=25, bg="white", border=0)
    signin_username.place(x=100, y=190)
    signin_username.insert(0, "Username")
    signin_username.bind("<FocusIn>", on_enter3)
    signin_username.bind("<FocusOut>", on_leave3)

    line1 = Frame(signin_frame, width=375, height=2, bg="black")
    line1.place(x=90, y=230)

    signin_password = Entry(signin_frame, fg="black", font=("Microsoft YaHei UI Light", 20), width=25, bg="white", border=0)
    signin_password.place(x=100, y=270)
    signin_password.insert(0, "Password")
    signin_password.bind("<FocusIn>", on_enter4)
    signin_password.bind("<FocusOut>", on_leave4)

    eyeopen_img3 = PhotoImage(file="Assets/openeye.png")
    eyeopen_btn3 = Button(signin_frame, image=eyeopen_img3, bg="white", border=0, activebackground="white", command=hide3)
    eyeopen_btn3.place(x=430, y=270)

    line2 = Frame(signin_frame, width=375, height=2, bg="black")
    line2.place(x=90, y=310)

    signin_btn = Button(signin_frame, text="SignIn", font=("Roboto", 20), padx=145, fg="white", bg="#19A7CE", cursor="hand2", command=lambda:sign_in(signin_username, signin_password, signin_Email))
    signin_btn.place(x=87, y=370)

    login = Label(signin_frame, text="Already have an Account?", font=("Microsoft YaHei UI Light", 11), bg="white")
    login.place(x=150, y=450)

    login_btn = Button(signin_frame, text="login", font=("Microsoft YaHei UI Light", 11), bg="white", border=0, fg="#19A7CE", cursor="hand2", command=login_frame)
    login_btn.place(x=330, y=448)

def Homepage():
    intro_root.destroy()
    call(["python", "main.py"])


def adminpage():
    intro_root.destroy()
    call(["python", "Adminpage.py"])


if __name__ == '__main__':
    login()
