from tkinter import *
from tkinter.ttk import Treeview
import pymysql
from tkinter import messagebox

def logout():
    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()
        query = "use users"
        mycursor.execute(query)

        query2 = "UPDATE userdata SET login_status = 0 where username = 'admin'"
        mycursor.execute(query2)
        con.commit()

        messagebox.showinfo("Logout", "Admin Logout")
    except Exception as e:
        print(e)

    admin_root.destroy()


def adminPage():
    global admin_root
    global dashboard_img
    global books_img
    global users_img
    global logout_img
    admin_root = Tk()
    admin_root.title("Admin Page")
    admin_root.geometry("1920x1080")
    sidebar = Frame(admin_root, width=250, height=1080, bg="#132043")
    sidebar.place(x=0, y=0)

    sidebar_img = PhotoImage(file="Assets//Admin.png", width=30, height=30)
    sidebar_img_lbl = Label(sidebar, image=sidebar_img, bg="#132043")
    sidebar_img_lbl.place(x=15, y=32)

    sidebar_title = Label(sidebar, text="AdminPage", font=("Roboto", 25), bg="#132043", fg="white")
    sidebar_title.place(x=50, y=30)

    dashboard_img = PhotoImage(file="Assets//Dashboard.png")
    dashboard_img_lbl = Label(sidebar, image=dashboard_img, bg="#132043")
    dashboard_img_lbl.place(x=15, y=155)

    books_img = PhotoImage(file="Assets//books.png")
    books_img_lbl = Label(sidebar, image=books_img, bg="#132043")
    books_img_lbl.place(x=15, y=260)

    users_img = PhotoImage(file="Assets//user.png")
    users_img_lbl = Label(sidebar, image=users_img, bg="#132043")
    users_img_lbl.place(x=15, y=360)

    logout_img = PhotoImage(file="Assets//logout.png")
    logout_img_lbl = Label(sidebar, image=logout_img, bg="#132043")
    logout_img_lbl.place(x=15, y=460)

    Dashboard_btn = Button(sidebar, text="Dashboard", font=("Roboto", 20), bg="white", fg="#132043", command=Dashboard)
    Dashboard_btn.place(x=70, y=150)

    Books_btn = Button(sidebar, text="Books", font=("Roboto", 20), bg="white", fg="#132043", padx=30, command=Books)
    Books_btn.place(x=70, y=250)

    Users_btn = Button(sidebar, text="Users", font=("Roboto", 20), bg="white", fg="#132043", padx=34, command=users)
    Users_btn.place(x=70, y=350)

    Users_btn = Button(sidebar, text="Logout", font=("Roboto", 20), bg="white", fg="#132043", padx=29, command=logout)
    Users_btn.place(x=70, y=450)

    Dashboard()

    admin_root.mainloop()

def Dashboard():
    global users
    global count
    global email
    global username
    global feedback
    global rating
    global count_feed
    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()
        query = "use users"
        mycursor.execute(query)

        query2 = "SELECT username FROM userdata WHERE subscribe = 1"
        mycursor.execute(query2)
        users = mycursor.fetchall()

        query3 = "SELECT COUNT(username) FROM userdata WHERE subscribe = 1"
        mycursor.execute(query3)
        count = mycursor.fetchone()[0]

        query4 = "SELECT Email FROM userdata WHERE subscribe = 1"
        mycursor.execute(query4)
        email = mycursor.fetchall()

        query5 = "use feedback"
        mycursor.execute(query5)

        query9 = "SELECT COUNT(username) FROM feed"
        mycursor.execute(query9)
        count_feed = mycursor.fetchone()[0]

        query6 = "SELECT username FROM feed"
        mycursor.execute(query6)
        username = mycursor.fetchall()

        query7 = "SELECT feedback FROM feed"
        mycursor.execute(query7)
        feedback = mycursor.fetchall()

        query8 = "SELECT rating FROM feed"
        mycursor.execute(query8)
        rating = mycursor.fetchall()

    except Exception as e:
        print(e)

    Dashboard_frame = Frame(admin_root, width=1650, height=1080, bg="#AEDEFC")
    Dashboard_frame.place(x=250, y=0)

    Title = Label(Dashboard_frame, text="Dashboard", font=('Microsoft YaHei UI Light', 35, 'bold'), bg="#AEDEFC")
    Title.place(x=50, y=50)

    Title_line = Frame(Dashboard_frame, width=250, height=2, bg="black")
    Title_line.place(x=50, y=130)

    Users_online = Label(Dashboard_frame, text="Users Subscribed", font=('Microsoft YaHei UI Light', 15, 'bold'), bg="#AEDEFC")
    Users_online.place(x=100, y=200)

    Feedback_lbl = Label(Dashboard_frame, text="Books Feedback", font=('Microsoft YaHei UI Light', 15, 'bold'), bg="#AEDEFC")
    Feedback_lbl.place(x=650, y=200)

    table = Treeview(Dashboard_frame, columns=("Users", "UserEmail"), show="headings")
    table.place(x=0, y=250)

    table.heading("#1", text="User")
    table.heading("#2", text="User mail")

    table.column("#1", anchor=CENTER)
    table.column("#2", anchor=CENTER)


    for x in range(count):
        table.insert("", "end", values=(users[x], email[x]))


    scrollbar = Scrollbar(Dashboard_frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)

    scrollbar.place(x=390, y=252, height=220)

    table2 = Treeview(Dashboard_frame, columns=("username", "Book Name", "Rating"), show="headings")
    table2.place(x=420, y=250)

    table2.heading("#1", text="Book Name")
    table2.heading("#2", text="Feedback")
    table2.heading("#3", text="Rating")


    table2.column("#1", anchor=CENTER)
    table2.column("#3", anchor=CENTER)

    for x in range(count_feed):
        table2.insert("", "end", values=(username[x], feedback[x], rating[x]))

    scrollbar2 = Scrollbar(Dashboard_frame, orient="vertical", command=table2.yview)
    table2.configure(yscrollcommand=scrollbar2.set)

    scrollbar2.place(x=1010, y=252, height=220)


def Books():
    global BookNames
    global AuthorName
    global Catagory
    global BookRating
    global b_count
    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()
        query = "use library_books"
        mycursor.execute(query)

        query2 = "SELECT BookName FROM library"
        mycursor.execute(query2)
        BookNames = mycursor.fetchall()

        query3 = "SELECT BookAuthor FROM library"
        mycursor.execute(query3)
        AuthorName = mycursor.fetchall()

        query4 = "SELECT BookCatagory FROM library"
        mycursor.execute(query4)
        Catagory = mycursor.fetchall()

        query5 = "SELECT BookRating FROM library"
        mycursor.execute(query5)
        BookRating = mycursor.fetchall()

        query6 = "SELECT COUNT(BookID) FROM library"
        mycursor.execute(query6)
        b_count = mycursor.fetchone()[0]

    except Exception as e:
        print(e)



    Books_frame = Frame(admin_root, width=1650, height=1080, bg="#AEDEFC")
    Books_frame.place(x=250, y=0)

    Title = Label(Books_frame, text="Books Info", font = ('Microsoft YaHei UI Light', 35, 'bold'), bg = "#AEDEFC")
    Title.place(x=50, y=50)

    Title_line = Frame(Books_frame, width=250, height=2, bg="black")
    Title_line.place(x=50, y=130)

    table3 = Treeview(Books_frame, columns=("Book", "Author", "Category", "Rating"), show="headings")
    table3.place(x=50, y=180)

    table3.heading("#1", text="Book")
    table3.heading("#2", text="Author")
    table3.heading("#3", text="Category")
    table3.heading("#4", text="Rating")


    table3.column("#1", anchor=CENTER)
    table3.column("#2", anchor=CENTER)
    table3.column("#3", anchor=CENTER)
    table3.column("#4", anchor=CENTER)

    for x in range(b_count):
        table3.insert("", "end", values=(BookNames[x], AuthorName[x], Catagory[x], BookRating[x]))

    scrollbar3 = Scrollbar(Books_frame, orient="vertical", command=table3.yview)
    table3.configure(yscrollcommand=scrollbar3.set)

    scrollbar3.place(x=850, y=183, height=220)


def users():
    global user_username
    global user_Email
    global user_login_status
    global user_subscribe
    global user_count
    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()
        query = "use users"
        mycursor.execute(query)

        query6 = "SELECT COUNT(username) FROM userdata"
        mycursor.execute(query6)
        user_count = mycursor.fetchone()[0]

        query2 = "SELECT username FROM userdata"
        mycursor.execute(query2)
        user_username = mycursor.fetchall()

        query3 = "SELECT Email FROM userdata"
        mycursor.execute(query3)
        user_Email = mycursor.fetchall()

        query4 = "SELECT login_status FROM userdata"
        mycursor.execute(query4)
        user_login_status = mycursor.fetchall()

        query5 = "SELECT subscribe FROM userdata"
        mycursor.execute(query5)
        user_subscribe = mycursor.fetchall()



    except Exception as e:
        print(e)

    users_frame = Frame(admin_root, width=1650, height=1080, bg="#AEDEFC")
    users_frame.place(x=250, y=0)

    Title = Label(users_frame, text="Users Info", font=('Microsoft YaHei UI Light', 35, 'bold'), bg="#AEDEFC")
    Title.place(x=50, y=50)

    Title_line = Frame(users_frame, width=250, height=2, bg="black")
    Title_line.place(x=50, y=130)

    table3 = Treeview(users_frame, columns=("Username", "Email", "Subscription", "Login_Status"), show="headings")
    table3.place(x=50, y=180)

    table3.heading("#1", text="Username")
    table3.heading("#2", text="Email")
    table3.heading("#3", text="Subscription")
    table3.heading("#4", text="Login_Status")

    table3.column("#1", anchor=CENTER)
    table3.column("#2", anchor=CENTER)
    table3.column("#3", anchor=CENTER)
    table3.column("#4", anchor=CENTER)

    for x in range(user_count):
        table3.insert("", "end", values=(user_username[x], user_Email[x], user_subscribe[x], user_login_status[x]))

    scrollbar3 = Scrollbar(users_frame, orient="vertical", command=table3.yview)
    table3.configure(yscrollcommand=scrollbar3.set)

    scrollbar3.place(x=850, y=183, height=220)

if __name__ == '__main__':
    adminPage()