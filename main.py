from tkinter import *
from tkinter import Scrollbar
from tkinter import messagebox
import pymysql
import webbrowser as wb
import tempfile
from PIL import Image, ImageTk
import smtplib
import random


def on_enter(e):
    search.delete(0, "end")

def on_leave(e):
    name = search.get()
    if name == '':
        search.insert(0, "Search")

def on_enter2(e):
    feedback_inputs.delete(1.0, "end-1c")

def on_leave2(e):
    name = feedback_inputs.get(1.0, "end-1c")
    if name == '':
        feedback_inputs.insert(1.0, "Feedback")




def back():
    Pre_frame.place_forget()

def back2():
    pur_frame.place_forget()

def back4():
    Pre_frame2.place_forget()


def preview(button_pressed):
    global Pre_frame
    global Prev_back_img
    global Bookimg_img
    global mycursor
    global Libbook_lbl3
    global book_img
    Pre_frame = Frame(homeFrame, width=500, height=500, bg="white")
    Pre_frame.place(x=280,y=20)

    button_pressed = int(button_pressed)

    Prev_back_img = PhotoImage(file="Assets//Back.png")
    Prev_Back_btn = Button(Pre_frame, image=Prev_back_img, command=back, bg="white", border=0, activebackground="white")
    Prev_Back_btn.place(x=0, y=10)

    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()

    except FileNotFoundError:
        messagebox.showerror("ERROR", "Connection Lost!!")

    query = "use library_books"
    mycursor.execute(query)
    query2 = "select BookName from library where BookID=%s"
    mycursor.execute(query2, (button_pressed))
    book_name = mycursor.fetchone()
    query3 = "select BookAuthor from library where BookID=%s"
    mycursor.execute(query3, (button_pressed))
    book_author_name=mycursor.fetchone()
    query4 = "select BookInfo from library where BookID=%s"
    mycursor.execute(query4, (button_pressed))
    book_info = mycursor.fetchone()
    query5 = "select BookImg from library where BookID=%s"
    mycursor.execute(query5, (button_pressed))
    book_img = mycursor.fetchone()[0]
    query6 = "select BookRating from library where BookID=%s"
    mycursor.execute(query6, (button_pressed))
    book_rating= mycursor.fetchone()[0]

    if book_name and book_author_name:
        Head = Label(Pre_frame, text=book_name[0], font=("Microsoft YaHei UI Light", 20), bg="white")
        Head.place(x=50, y=10)

        Author = Label(Pre_frame, text=f"By {book_author_name[0]}", font=("Times", 15), bg="white")
        Author.place(x=50, y=50)

        line = Frame(Pre_frame, width=150, height=2, bg="blue")
        line.place(x=50, y=80)

        if book_img is not None:
            with open("temp_image.jpg", "wb") as temp_file:
                temp_file.write(book_img)

            # Open the image using PIL
            image = Image.open("temp_image.jpg")

            # Create a PhotoImage from the PIL image
            book_img = ImageTk.PhotoImage(image)
            Libbook_lbl3 = Label(Pre_frame)
            Libbook_lbl3.config(image=book_img)
            Libbook_lbl3.place(x=50, y=100)
        else:
            Libbook_lbl3.config(image=None)

        Book_rating = Label(Pre_frame, text=f"Rating: {book_rating} Stars", font=("Microsoft YaHei UI Light", 10), bg="yellow")
        Book_rating.place(x=50, y=410)

        Ab = Label(Pre_frame, text="About:", font=("Microsoft YaHei UI Light", 20), bg="white")
        Ab.place(x=280, y=80)

        About = Label(Pre_frame, text=book_info[0], font=("Times", 10), bg="#F7E6C4",  wraplength=200)
        About.place(x=280, y=120)


def purchase(button_id):
    global pur_frame
    global Pur_back_img
    global check2
    global check1
    global check3
    global user
    global IMG
    global username_input
    global Password_input
    button_id = int(button_id)
    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()
        query = "use users"
        mycursor.execute(query)
        query4 = "select username from userData where login_status=1 and subscribe=1"
        mycursor.execute(query4)
        user = mycursor.fetchone()

    except FileNotFoundError:
        messagebox.showerror("ERROR", "Connection Lost!!")

    if user:
        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor = con.cursor()
            query = "use library_books"
            mycursor.execute(query)
            query2 = "select BookPdfs from library where BookID=%s"
            mycursor.execute(query2, (button_id))
            check3 = mycursor.fetchone()[0]
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
                temp_pdf_file.write(check3)
                temp_pdf_file_path = temp_pdf_file.name

            # Open the temporary PDF file in the default web browser
            wb.open(temp_pdf_file_path)

        except FileNotFoundError:
            messagebox.showerror("ERROR", "Connection Lost!!")

    elif not user:
        pur_frame = Frame(homeFrame, width=400, height=300, bg="white")
        pur_frame.place(x=340, y=20)

        Pur_back_img = PhotoImage(file="Assets//Back.png")
        Pur_Back_btn = Button(pur_frame, image=Pur_back_img, command=back2, bg="white", border=0, activebackground="white")
        Pur_Back_btn.place(x=0, y=10)

        heading_lbl = Label(pur_frame, text="Subscription: ", font=("Roboto", 15), bg="white")
        heading_lbl.place(x=50, y=15)

        line_frame = Frame(pur_frame, width=300, height=2, bg="black")
        line_frame.place(x=50, y=45)

        username_lbl = Label(pur_frame, text="Username", font=('Roboto', 15), bg="white")
        username_lbl.place(x=50, y=100)

        username_input = Entry(pur_frame)
        username_input.place(x=200, y=100)

        Password_lbl = Label(pur_frame, text="Password", font=('Roboto', 15), bg="white")
        Password_lbl.place(x=50, y=140)

        Password_input = Entry(pur_frame)
        Password_input.place(x=200, y=140)

        Submit_btn = Button(pur_frame, text="Submit", bg='cyan', fg="black", font=("Roboto", 15), padx=100, command=mail)
        Submit_btn.place(x=50, y=200)


def on_enter1(e):
    username_feed.delete(0, "end")

def on_leave1(e):
    name = username_feed.get()
    if name == '':
        username_feed.insert(0, "Username")


def Logout():
    global check
    global mycursor
    global conn
    try:
        conn = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = conn.cursor()
        query = "use users"
        mycursor.execute(query)
        query2 = "SELECT * FROM userdata where login_status=1"
        mycursor.execute(query2)
        check = mycursor.fetchone()


    except FileNotFoundError:
        messagebox.showerror("ERROR", "Connection Lost!!")

    if check:
        query3 = "UPDATE userdata SET login_status = 0"
        mycursor.execute(query3)
        conn.commit()
        messagebox.showinfo("Logged Out", "Logged out Successfully!")
        main_root.destroy()

    else:
        messagebox.showinfo("Alert!!", "Please check if you are logged in?")


def Submit_form():
    global user
    userfeed = username_feed.get()
    feedbackinput = feedback_inputs.get('1.0', END)
    Rate_box = Rating_box.get()
    if (username_feed.get() == "BookName"):
        username_feed.delete(0, "end")

    if (username_feed.get() == ""):
        messagebox.showerror("Error", "Feedback Not Feed!!")

    else:
        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor = con.cursor()
            try:
                con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
                mycursor = con.cursor()
                query = "use users"
                mycursor.execute(query)
                query4 = "select username from userData where login_status=1"
                mycursor.execute(query4)
                user = mycursor.fetchone()

            except FileNotFoundError:
                messagebox.showerror("ERROR", "Connection Lost!!")

            if user:
                try:
                    query = "use feedback"
                    mycursor.execute(query)
                    query2 = "INSERT INTO feed VALUES(%s, %s, %s)"
                    mycursor.execute(query2, (userfeed, feedbackinput, Rate_box))
                    con.commit()
                    query3 = "USE library_books"
                    mycursor.execute(query3)
                    query4 = "UPDATE library SET BookRating = %s WHERE BookName = %s"
                    mycursor.execute(query4, (Rate_box, userfeed))
                    con.commit()

                    messagebox.showinfo(f"Feedback For Book {userfeed} Registered successfully")

                    feedback_inputs.delete(1.0, "end-1c")
                    username_feed.delete(0, "end")

                except Exception as e:
                    print(e)

            else:
                messagebox.showerror("Error!!", "Not logdin")

        except Exception as e:
            print(e)


def mail():
    global userin
    global passin
    global pin_frame
    global Pur_back_img6
    global pin_input
    global num
    userin = username_input.get()
    passin = Password_input.get()

    if (userin == ""):
        messagebox.showerror("Error", "Username not Entered")

    elif (passin == ""):
        messagebox.showerror("Error", "Password not Entered")

    else:

        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor2 = con.cursor()
            query = "USE users"
            mycursor2.execute(query)

            query2 = "select username from userData where subscribe=0"
            mycursor2.execute(query2)
            subs = mycursor2.fetchone()

            query3 = "select Email from userData where username=%s"
            mycursor2.execute(query3, (userin))
            Email = mycursor2.fetchone()[0]

            if subs:
                random_number = random.randint(1000, 9999)
                num = str(random_number)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("snapbooks9@gmail.com", "lrkprjqmofvxatjp")
                server.sendmail("snapbooks9@gmail.com", Email, num)

                messagebox.showinfo("Mail", "Mail sent on the required mail address!!")

                pur_frame.place_forget()

                pin_frame = Frame(homeFrame, width=400, height=300, bg="white")
                pin_frame.place(x=340, y=20)

                Pur_back_img6 = PhotoImage(file="Assets//Back.png")
                Pur_Back_btn6 = Button(pin_frame, image=Pur_back_img6, command=back6, bg="white", border=0,
                                      activebackground="white")
                Pur_Back_btn6.place(x=0, y=10)

                heading_lbl = Label(pin_frame, text="Pin Sent on Mail: ", font=("Roboto", 15), bg="white")
                heading_lbl.place(x=50, y=15)

                line_frame = Frame(pin_frame, width=300, height=2, bg="black")
                line_frame.place(x=50, y=45)

                pin_lbl = Label(pin_frame, text="Pincode", font=('Roboto', 15), bg="white")
                pin_lbl.place(x=50, y=100)

                pin_input = Entry(pin_frame)
                pin_input.place(x=200, y=100)

                Submit_pin = Button(pin_frame, text="Submit", bg='cyan', fg="black", font=("Roboto", 15), padx=100, command=execute)
                Submit_pin.place(x=50, y=200)


            else:
                messagebox.showinfo("Info", "You are Already Subscribed!!")


        except Exception as e:
            print(e)


def execute():
    pin_number = pin_input.get()

    if pin_number == num:
        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor2 = con.cursor()
            query = "USE users"
            mycursor2.execute(query)

            query2 = "update userdata set subscribe = 1 where username = %s"
            mycursor2.execute(query2, userin)
            con.commit()

            messagebox.showinfo("Subscribe", "You Are Subscribed!!")

        except EXCEPTION as e:
            print(e)

    else:
        messagebox.showerror("Error", "Invalid Pincode!!")



def back6():
    pin_frame.place_forget()



def feedback_frame():
    # -------------Feedback Frame----------------#
    global feedback_f
    global feedback_img
    global username_feed
    global feedback_inputs
    global Rating_box
    feedback_f = Frame(main_root, width=1100, height=1080, bg="#FFF3DA")
    feedback_f.place(x=190, y=51)

    feedback_img = PhotoImage(file="Assets//Feedback.png")
    feedback_img_frame = Label(feedback_f, image=feedback_img, bg="#FFF3DA")
    feedback_img_frame.place(x=0, y=70)

    feed_label = Label(feedback_f, text="Books FeedBack: ", font=("Roboto", 40), border=0, bg="#FFF3DA", fg="#35155D")
    feed_label.place(x=70, y=20)

    username_feed = Entry(feedback_f, fg="black", font=("Microsoft YaHei UI Light", 20), width=25, bg="white")
    username_feed.place(x=490, y=160)
    username_feed.insert(0, "BookName")
    username_feed.bind("<FocusIn>", on_enter1)
    username_feed.bind("<FocusOut>", on_leave1)

    check_box_f = Frame(feedback_f, bg="#FFF3DA", width=250, height=100)
    check_box_f.place(x=490, y=230)

    check_box_label = Label(check_box_f, text="Rating Till 5 Star", bg="#FFF3DA", font=("Microsoft YaHei UI Light", 20), fg="black")
    check_box_label.place(x=0, y=0)

    Rating_box = Entry(check_box_f, fg="black", font=("Microsoft YaHei UI Light", 20), width=25, bg="white")
    Rating_box.place(x=0, y=40)

    compultion = Label(feedback_f, text="*Compulsory", font=("Roboto", 10), fg="Red", bg="#FFF3DA")
    compultion.place(x=490, y=130)

    feedback_inputs = Text(feedback_f, font=("Microsoft YaHei UI Light", 15), fg="Black", bg="white")
    feedback_inputs.place(x=490, y=350, height=100, width=550)
    feedback_inputs.insert(1.0, "Feedback")
    feedback_inputs.bind("<FocusIn>", on_enter2)
    feedback_inputs.bind("<FocusOut>", on_leave2)

    submit_btn = Button(feedback_f, text='Submit', bg="#AED2FF", activebackground="#AED2FF", fg="Black",
                        activeforeground='Black', font=("Microsoft YaHei UI Light", 22), border=0, cursor="hand2",
                        padx=80, command=Submit_form)
    submit_btn.place(x=490, y=460)



    hide_Indicators_Home()
    homeFrame.place_forget()
    hide_Indicators_Lib()
    lib_f.place_forget()

def hide_Indicators_Lib():
    Library_indicator.config(bg="black")

def on_configure(event):
    my_canvas.configure(scrollregion=my_canvas.bbox("all"))

def on_configure4(event):
    lib_my_canvas.configure(scrollregion=lib_my_canvas.bbox("all"))

def Hom_indicator():
    # -------------Home Frame----------------#
    global homeFrame
    global my_canvas
    global book_show_1_img
    global book_show_2_img
    global book_show_3_img
    global book_show_4_img
    global book_show_5_img
    global frame_books1
    global frame_books2
    global frame_books3
    global frame_books4
    global frame_books5
    global frame_books6
    global ID
    global book_Img_list
    global Libbook_lbl
    global main_frame_info2
    global name_book
    global ID2
    global book_Img_list2
    global book_Img_list3
    global ID3
    homeFrame = Frame(main_root, width=1100, height=1080, bg="#E3F4F4")
    homeFrame.place(x=190, y=51)

    book_show_1_img = PhotoImage(file="Assets//Book_show_1.png")
    book_show_2_img = PhotoImage(file="Assets//Book_shop_2.png")
    book_show_3_img = PhotoImage(file="Assets//Book_shop_3.png")
    book_show_4_img = PhotoImage(file="Assets//Book_shop_4.png")
    book_show_5_img = PhotoImage(file="Assets//Book_shop_5.png")


    my_canvas = Canvas(homeFrame ,width=1067, height=645)
    my_canvas.pack(side=LEFT)


    scrollbar = Scrollbar(homeFrame, command=my_canvas.yview, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind("<Configure>", on_configure)

    my_frame = Frame(my_canvas, bg="#E3F4F4")
    my_canvas.create_window((0,0), window=my_frame, anchor=NW)

    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor2 = con.cursor()
        query = "USE library_books"
        mycursor2.execute(query)

        query2 = "SELECT BookImg FROM library WHERE BookRating > 4 ORDER BY BookRating DESC"
        mycursor2.execute(query2)
        book_Img_list = mycursor2.fetchall()

        query4 = "SELECT BookID FROM library WHERE BookRating > 4 ORDER BY BookRating DESC"
        mycursor2.execute(query4)
        ID = mycursor2.fetchall()

        query5 = "SELECT BookImg FROM library WHERE BookRating > 3.7 AND BookRating < 4 ORDER BY BookRating DESC"
        mycursor2.execute(query5)
        book_Img_list2 = mycursor2.fetchall()

        query6 = "SELECT BookID FROM library WHERE BookRating > 3.7 AND BookRating < 4 ORDER BY BookRating DESC"
        mycursor2.execute(query6)
        ID2 = mycursor2.fetchall()

        query7 = "SELECT BookImg FROM library WHERE BookRating > 1 AND BookRating < 3.7 ORDER BY BookRating DESC"
        mycursor2.execute(query7)
        book_Img_list3 = mycursor2.fetchall()

        query8 = "SELECT BookID FROM library WHERE BookRating > 1 AND BookRating < 3.7 ORDER BY BookRating DESC"
        mycursor2.execute(query8)
        ID3 = mycursor2.fetchall()

    except Exception as e:
        print(e)

    for i in range(1):
        l2 = Label(my_frame, image= book_show_1_img)
        l2.pack()

    for i in range(1):
        frame_books1 = Frame(my_frame, width=1100, height=500, bg="White")
        frame_books1.pack()

    label1 = Label(frame_books1, text="Top Books Rated more than 4: ", font=('Microsoft YaHei UI Light', 20, "bold"), bg="white")
    label1.place(x=0, y=20)

    label1_line = Frame(frame_books1, height=2, width=400, bg="black")
    label1_line.place(x=0, y=60)

    main_frame_info = Frame(frame_books1, width=1065, height=419, bg="#D2E0FB")
    main_frame_info.place(x=0, y=80)

    ID = [item[0] for item in ID if item[0] != " "]
    for z in range(4):

        book_image_list = book_Img_list[z][0]


        if book_image_list is not None:

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', mode='wb')
            temp_file.write(book_image_list)
            temp_file.close()

            image = Image.open(temp_file.name)

            Libbook_img = ImageTk.PhotoImage(image)
            Libbook_lbl = Label(main_frame_info)
            Libbook_lbl.config(image=Libbook_img)
            Libbook_lbl.image = Libbook_img
            Libbook_lbl.grid(column=z, row=0, padx=70, pady=50)


        else:
            Libbook_lbl.config(image=None)

    main_frame_info21 = Frame(frame_books1, width=1065, height=40, bg="#D2E0FB")
    main_frame_info21.place(x=0, y=340)



    x_1 = [70, 340, 610, 885]
    x_2 = [150, 420, 690, 965]

    for y in range(4):
        name_book = ID[y]
        MDB_btnpur1 = Button(main_frame_info21, text="Purchase", font=('Microsoft YaHei UI Light', 10), command=lambda m=name_book: purchase(m)).place(x=x_1[y], y=0)
        MDB_btnpre1 = Button(main_frame_info21, text="Preview", font=('Microsoft YaHei UI Light', 10), command=lambda m=name_book: preview(m)).place(x=x_2[y], y=0)

    for i in range(1):
        l1 = Label(my_frame, image=book_show_2_img)
        l1.pack()

    for i in range(1):
        frame_books2 = Frame(my_frame, width=1100, height=500, bg="white")
        frame_books2.pack()

    label2 = Label(frame_books2, text="Top Books Rated more than 3:", font=('Microsoft YaHei UI Light', 20, "bold"), bg="white")
    label2.place(x=0, y=20)

    label1_line1 = Frame(frame_books2, height=2, width=400, bg="black")
    label1_line1.place(x=0, y=60)

    main_frame_info2 = Frame(frame_books2, width=1065, height=419, bg="#D2E0FB")
    main_frame_info2.place(x=0, y=80)

    ID2 = [item[0] for item in ID2 if item[0] != " "]

    for z in range(4):

        book_image_list = book_Img_list2[z][0]


        if book_image_list is not None:

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', mode='wb')
            temp_file.write(book_image_list)
            temp_file.close()

            image = Image.open(temp_file.name)

            Libbook_img = ImageTk.PhotoImage(image)
            Libbook_lbl = Label(main_frame_info2)
            Libbook_lbl.config(image=Libbook_img)
            Libbook_lbl.image = Libbook_img
            Libbook_lbl.grid(column=z, row=0, padx=70, pady=50)


        else:
            Libbook_lbl.config(image=None)

    main_frame_info22 = Frame(frame_books2, width=1065, height=40, bg="#D2E0FB")
    main_frame_info22.place(x=0, y=340)

    x_1 = [70, 340, 610, 885]
    x_2 = [150, 420, 690, 965]

    for y in range(4):
        name_book = ID2[y]
        MDB_btnpur1 = Button(main_frame_info22, text="Purchase", font=('Microsoft YaHei UI Light', 10), command=lambda m=name_book: purchase(m)).place(x=x_1[y], y=0)
        MDB_btnpre1 = Button(main_frame_info22, text="Preview", font=('Microsoft YaHei UI Light', 10), command=lambda m=name_book: preview(m)).place(x=x_2[y], y=0)


    for i in range(1):
        l1 = Label(my_frame, image=book_show_3_img)
        l1.pack()

    for i in range(1):
        frame_books3 = Frame(my_frame, width=1100, height=500, bg="white")
        frame_books3.pack()

    label3 = Label(frame_books3, text="Top Books Rated more than 1:", font=('Microsoft YaHei UI Light', 20, "bold"), bg="white")
    label3.place(x=0, y=20)

    label1_line3 = Frame(frame_books3, height=2, width=400, bg="black")
    label1_line3.place(x=0, y=60)

    main_frame_info3 = Frame(frame_books3, width=1065, height=419, bg="#D2E0FB")
    main_frame_info3.place(x=0, y=80)


    ID3 = [item[0] for item in ID3 if item[0] != " "]

    for z in range(4):

        book_image_list = book_Img_list3[z][0]


        if book_image_list is not None:

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', mode='wb')
            temp_file.write(book_image_list)
            temp_file.close()

            image = Image.open(temp_file.name)

            Libbook_img = ImageTk.PhotoImage(image)
            Libbook_lbl = Label(main_frame_info3)
            Libbook_lbl.config(image=Libbook_img)
            Libbook_lbl.image = Libbook_img
            Libbook_lbl.grid(column=z, row=0, padx=70, pady=50)


        else:
            Libbook_lbl.config(image=None)

    main_frame_info23 = Frame(frame_books3, width=1065, height=40, bg="#D2E0FB")
    main_frame_info23.place(x=0, y=340)

    x_1 = [70, 340, 610, 885]
    x_2 = [150, 420, 690, 965]

    for y in range(4):
        name_book = ID3[y]
        MDB_btnpur1 = Button(main_frame_info23, text="Purchase", font=('Microsoft YaHei UI Light', 10), command=lambda m=name_book: purchase(m)).place(x=x_1[y], y=0)
        MDB_btnpre1 = Button(main_frame_info23, text="Preview", font=('Microsoft YaHei UI Light', 10), command=lambda m=name_book: preview(m)).place(x=x_2[y], y=0)


    hide_Indicators_Lib()
    Home_indicator.config(bg="white")
    feedback_f.place_forget()
    lib_f.place_forget()

def hide_Indicators_Home():
    Home_indicator.config(bg="black")

def preview2(button_pressed):
    global Pre_frame2
    global Prev_back_img2
    global Bookimg_img
    global mycursor2
    global Libbook_lbl2
    global book_img2
    global Libbook_lbl3
    Pre_frame2 = Frame(lib_f, width=500, height=500, bg="white")
    Pre_frame2.place(x=280,y=20)

    Prev_back_img2 = PhotoImage(file="Assets//Back.png")
    Prev_Back_btn2 = Button(Pre_frame2, image=Prev_back_img2, command=back4, bg="white", border=0, activebackground="white")
    Prev_Back_btn2.place(x=0, y=10)

    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor2 = con.cursor()

    except FileNotFoundError:
        messagebox.showerror("ERROR", "Connection Lost!!")

    query = "use library_books"
    mycursor2.execute(query)
    query2 = "select BookName from library where BookID=%s"
    mycursor2.execute(query2, (button_pressed))
    book_name = mycursor2.fetchone()
    query3 = "select BookAuthor from library where BookID=%s"
    mycursor2.execute(query3, (button_pressed))
    book_author_name=mycursor2.fetchone()
    query4 = "select BookInfo from library where BookID=%s"
    mycursor2.execute(query4, (button_pressed))
    book_info = mycursor2.fetchone()[0]
    query5 = "select BookImg from library where BookID=%s"
    mycursor2.execute(query5, (button_pressed))
    book_img2=mycursor2.fetchone()[0]
    query6 = "select BookRating from library where BookID=%s"
    mycursor2.execute(query6, (button_pressed))
    book_rating= mycursor2.fetchone()[0]
    if book_img2 is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', mode='wb')
        temp_file.write(book_img2)
        temp_file.close()

        image2 = Image.open(temp_file.name)

        Libbook_img3 = ImageTk.PhotoImage(image2)
        Libbook_lbl3 = Label(Pre_frame2)
        Libbook_lbl3.config(image=Libbook_img3)
        Libbook_lbl3.image = Libbook_img3
        Libbook_lbl3.place(x=50, y=140)
    else:
        Libbook_lbl3.config(image=None)



    if book_name:
        Head2 = Label(Pre_frame2, text=book_name[0], font=("Microsoft YaHei UI Light", 20), bg="white")
        Head2.place(x=50, y=10)

        Author2 = Label(Pre_frame2, text=f"By {book_author_name[0]}", font=("Times", 15), bg="white")
        Author2.place(x=50, y=50)

        line2 = Frame(Pre_frame2, width=150, height=2, bg="blue")
        line2.place(x=50, y=80)



        Book_rating2 = Label(Pre_frame2, text=f"Rating: {book_rating} Stars", font=("Microsoft YaHei UI Light", 10), bg="yellow")
        Book_rating2.place(x=50, y=410)

        Ab2 = Label(Pre_frame2, text="About:", font=("Microsoft YaHei UI Light", 20), bg="white")
        Ab2.place(x=280, y=80)

        About2 = Label(Pre_frame2, text=book_info, font=("Times", 10), bg="#F7E6C4",  wraplength=200)
        About2.place(x=280, y=120)

def mail2():
    global userin
    global passin
    global pin_frame
    global Pur_back_img7
    global pin_input
    global num
    userin = username_input.get()
    passin = Password_input.get()

    if (userin == ""):
        messagebox.showerror("Error", "Username not Entered")

    elif (passin == ""):
        messagebox.showerror("Error", "Password not Entered")

    else:

        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor2 = con.cursor()
            query = "USE users"
            mycursor2.execute(query)

            query2 = "select username from userData where subscribe=0"
            mycursor2.execute(query2)
            subs = mycursor2.fetchone()

            query3 = "select Email from userData where username=%s"
            mycursor2.execute(query3, (userin))
            Email = mycursor2.fetchone()[0]

            if subs:
                random_number = random.randint(1000, 9999)
                num = str(random_number)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("snapbooks9@gmail.com", "lrkprjqmofvxatjp")
                server.sendmail("snapbooks9@gmail.com", Email, num)

                messagebox.showinfo("Mail", "Mail sent on the required mail address!!")

                pur_frame2.place_forget()

                pin_frame = Frame(lib_f, width=400, height=300, bg="white")
                pin_frame.place(x=340, y=20)

                Pur_back_img7 = PhotoImage(file="Assets//Back.png")
                Pur_Back_btn7 = Button(pin_frame, image=Pur_back_img7, command=back7, bg="white", border=0,
                                      activebackground="white")
                Pur_Back_btn7.place(x=0, y=10)

                heading_lbl = Label(pin_frame, text="Pin Sent on Mail: ", font=("Roboto", 15), bg="white")
                heading_lbl.place(x=50, y=15)

                line_frame = Frame(pin_frame, width=300, height=2, bg="black")
                line_frame.place(x=50, y=45)

                pin_lbl = Label(pin_frame, text="Pincode", font=('Roboto', 15), bg="white")
                pin_lbl.place(x=50, y=100)

                pin_input = Entry(pin_frame)
                pin_input.place(x=200, y=100)

                Submit_pin = Button(pin_frame, text="Submit", bg='cyan', fg="black", font=("Roboto", 15), padx=100, command=execute2)
                Submit_pin.place(x=50, y=200)


            else:
                messagebox.showinfo("Info", "You are Already Subscribed!!")


        except Exception as e:
            print(e)


def execute2():
    pin_number = pin_input.get()

    if pin_number == num:
        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor2 = con.cursor()
            query = "USE users"
            mycursor2.execute(query)

            query2 = "update userdata set subscribe = 1 where username = %s"
            mycursor2.execute(query2, userin)
            con.commit()

            messagebox.showinfo("Subscribe", "You Are Subscribed!!")

        except EXCEPTION as e:
            print(e)

    else:
        messagebox.showerror("Error", "Invalid Pincode!!")



def back7():
    pin_frame.place_forget()

def pur2(button_id):
    global pur_frame2
    global Pur_back_img2
    global user2
    global username_input
    global Password_input
    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()
        query = "use users"
        mycursor.execute(query)
        query4 = "select username from userData where login_status=1 and subscribe=1"
        mycursor.execute(query4)
        user2 = mycursor.fetchone()

    except FileNotFoundError:
        messagebox.showerror("ERROR", "Connection Lost!!")

    if user2:
        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor = con.cursor()
            query = "use library_books"
            mycursor.execute(query)
            query2 = "select BookPdfs from library where BookID=%s"
            mycursor.execute(query2, (button_id))
            check4 = mycursor.fetchone()[0]
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
                temp_pdf_file.write(check4)
                temp_pdf_file_path = temp_pdf_file.name

            # Open the temporary PDF file in the default web browser
            wb.open(temp_pdf_file_path)

        except FileNotFoundError:
            messagebox.showerror("ERROR", "Connection Lost!!")

    elif not user2:
        pur_frame2 = Frame(lib_f, width=400, height=300, bg="white")
        pur_frame2.place(x=340, y=20)

        Pur_back_img2 = PhotoImage(file="Assets//Back.png")
        Pur_Back_btn = Button(pur_frame2, image=Pur_back_img2, command=back5, bg="white", border=0, activebackground="white")
        Pur_Back_btn.place(x=0, y=10)

        heading_lbl = Label(pur_frame2, text="Subscribe:", font=("Roboto", 15), bg="white")
        heading_lbl.place(x=50, y=15)

        line_frame = Frame(pur_frame2, width=300, height=2, bg="black")
        line_frame.place(x=50, y=45)

        username_lbl = Label(pur_frame2, text="Username", font=('Roboto', 15), bg="white")
        username_lbl.place(x=50, y=100)

        username_input = Entry(pur_frame2)
        username_input.place(x=200, y=100)

        Password_lbl = Label(pur_frame2, text="Password", font=('Roboto', 15), bg="white")
        Password_lbl.place(x=50, y=140)

        Password_input = Entry(pur_frame2)
        Password_input.place(x=200, y=140)

        Submit_btn = Button(pur_frame2, text="Submit", bg='cyan', fg="black", font=("Roboto", 15), padx=100,
                            command=mail2)
        Submit_btn.place(x=50, y=200)

def back5():
    pur_frame2.place_forget()

def Lib_indicator():
    global lib_f
    global lib1
    global lib_my_canvas
    global frame_lib
    global libbooks_name
    global img_data
    global libbook_img
    global image
    global Libbook_lbl
    global books_frame
    global Libbook_img
    global selected_option
    global lib_my_frame
    global cat_frm
    global selected_option
    global name
    lib_f = Frame(main_root, width= 1100, height= 1080, bg="#B1AFFF")
    lib_f.place(x=190, y=51)

    lib_my_canvas = Canvas(lib_f, width=1067, height=645)
    lib_my_canvas.pack(side=LEFT)

    lib_scrollbar = Scrollbar(lib_f, command=lib_my_canvas.yview, orient=VERTICAL)
    lib_scrollbar.pack(side=RIGHT, fill=Y)

    lib_my_canvas.configure(yscrollcommand=lib_scrollbar.set)
    lib_my_canvas.bind("<Configure>", on_configure4)

    lib_my_frame = Frame(lib_my_canvas, bg="white")
    lib_my_canvas.create_window((0, 0), window=lib_my_frame, anchor=NW)

    start = 601
    books_inc = 601
    end = 652
    row = 0

    cat_frm = Frame(lib_my_frame, bg="white", width=200, height=100)
    cat_frm.place(x=950, y=0)

    cat_frm2 = Frame(lib_my_frame, bg="white", width=200, height=100)
    cat_frm2.place(x=0, y=0)


    Cat_Label = Label(cat_frm2, text="Category", font=('Microsoft YaHei UI Light', 10, 'bold'), bg="white")
    Cat_Label.place(x=0, y=0)




    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12", database="library_books")
        mycursor = con.cursor()

        query = "use library_books"
        mycursor.execute(query)

        query2 = "SELECT DISTINCT BookCatagory FROM library"
        mycursor.execute(query2)

        categories = mycursor.fetchall()  # Fetch all categories

        if categories:
            # Create a Tkinter window

            # Create a StringVar to store the selected category
            selected_option = StringVar(cat_frm)

            # Extract category names from the fetched data
            category_names = [cat[0] for cat in categories]

            # Create the dropdown menu
            dropdown_menu = OptionMenu(cat_frm, selected_option, *category_names)
            dropdown_menu.pack(pady=2)

            name = "Category List"

            # Set the initial selection (optional)
            selected_option.set(name)

            dropdown_menu.bind("<Configure>", get_selected_category)

            # Function to retrieve the selected category


        else:
            print("No categories found in the database.")

    except Exception as e:
        print(f"Connection Lost! {e}")

    for i in range(start, end + 1):
        try:
            conn = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor = conn.cursor()
            query = "use library_books"
            mycursor.execute(query)
            query2 = "SELECT BookName FROM library WHERE BookId=%s"
            mycursor.execute(query2, (books_inc))
            libbooks_name = mycursor.fetchone()[0]
            query3 = "select BookImg from library where BookID=%s"
            mycursor.execute(query3, (books_inc))
            libbook_img = mycursor.fetchone()[0]
            query4 = "select BookAuthor from library where BookID=%s"
            mycursor.execute(query4, (books_inc))
            book_author = mycursor.fetchone()[0]

            books_frame = Frame(lib_my_frame, width=1100, height=300, bg="#E5CFF7")
            books_frame.grid(row=row, pady=28)

            label = Label(books_frame, text=str(libbooks_name), font=('Microsoft YaHei UI Light', 25, 'bold'), bg="#E5CFF7", fg="black")
            label.place(x=200, y=50)

            Author_label = Label(books_frame, text=str(book_author), font=('Roboto', 15), bg="#E5CFF7", fg="black")
            Author_label.place(x=200, y=100)

            Prev_button = Button(books_frame, text="Preview", font=('Microsoft YaHei UI Light', 15), bg="#FF6969", fg="white",activebackground="#FF6969", command=lambda id=books_inc: preview2(id))
            Prev_button.place(x=320, y=150)

            Pur_button = Button(books_frame, text="Purchase", font=('Microsoft YaHei UI Light', 15), bg="#FF6969", fg="white",activebackground="#FF6969", command=lambda id=books_inc: pur2(id))
            Pur_button.place(x=205, y=150)

            Pur_button = Button(books_frame, text="Feedback", font=('Microsoft YaHei UI Light', 15), bg="grey", fg="white", activebackground="grey", command=feedback_frame)
            Pur_button.place(x=425, y=150)

            if libbook_img is not None:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', mode='wb')
                temp_file.write(libbook_img)
                temp_file.close()

                image = Image.open(temp_file.name)

                Libbook_img = ImageTk.PhotoImage(image)
                Libbook_lbl = Label(books_frame)
                Libbook_lbl.config(image=Libbook_img)
                Libbook_lbl.image = Libbook_img
                Libbook_lbl.place(x=50, y=50)

            else:
                Libbook_lbl.config(image=None)

        except FileNotFoundError:
            messagebox.showerror("ERROR", "Connection Lost!!")

        row += 1
        books_inc +=1

    Library_indicator.config(bg="white")
    hide_Indicators_Home()
    feedback_f.place_forget()
    homeFrame.place_forget()



def get_selected_category(event):
    global back_btn_img
    global selected_option
    global last_selected_category
    global new_frame
    global book_name
    global lib_my_canvas
    global btn_frame
    global Libbook_lbl
    global cat_books_frame
    global lib_my_frame
    selected_category = selected_option.get()
    last_selected_category = selected_category

    if selected_category == "Category List":
        return

    else:
        btn_frame = Frame(lib_f, width=1100, height=80,bg="white")
        btn_frame.place(x=0, y=0)

        back_btn_img = PhotoImage(file="Assets//back.png")
        back_btn = Button(btn_frame, image=back_btn_img, bg="white", command=back_btn_func)
        back_btn.place(x=10, y=20)

        new_lable = Label(btn_frame, text=f"Category: {selected_category}", font=("Roboto", 20), bg="white")
        new_lable.place(x=50, y=20)

        new_frame = Frame(lib_f, width=1100, height=1080, bg="white")
        new_frame.place(x=0, y=80)

        lib_my_canvas = Canvas(new_frame, width=1067, height=645)
        lib_my_canvas.pack(side=LEFT)

        lib_scrollbar = Scrollbar(new_frame, command=lib_my_canvas.yview, orient=VERTICAL)
        lib_scrollbar.pack(side=RIGHT, fill=Y)

        lib_my_canvas.configure(yscrollcommand=lib_scrollbar.set)
        lib_my_canvas.bind("<Configure>", on_configure9)

        lib_my_frame = Frame(lib_my_canvas, bg="white")
        lib_my_canvas.create_window((0, 0), window=lib_my_frame, anchor=NW)

        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12", database="library_books")
            mycursor = con.cursor()

            query = "use library_books"
            mycursor.execute(query)

            query2 = "SELECT BookName FROM library WHERE BookCatagory = %s"
            mycursor.execute(query2, (selected_category))
            catBooks = mycursor.fetchall()

            query3 = "SELECT BookAuthor FROM library WHERE BookCatagory = %s"
            mycursor.execute(query3, (selected_category))
            catBooks2 = mycursor.fetchall()

            query5 = "SELECT BookImg FROM library WHERE BookCatagory = %s"
            mycursor.execute(query5, (selected_category))
            catimg = mycursor.fetchall()

            query6 = "SELECT BookID FROM library WHERE BookCatagory = %s"
            mycursor.execute(query6, (selected_category))
            catid = mycursor.fetchall()

            query4 = "SELECT COUNT(*) AS book_count FROM library WHERE BookCatagory = %s"
            mycursor.execute(query4, (selected_category))
            catBooks3 = mycursor.fetchone()[0]

            catBooks = [item[0] for item in catBooks if item[0] != " "]
            catBooks2 = [item[0] for item in catBooks2 if item[0] != " "]

            for x in range(catBooks3):

                cat_books_frame = Frame(lib_my_frame, width=1100, height=300, bg="#FFCF96")
                cat_books_frame.grid(row=x, column=0, sticky="w", pady=50)


                book_name = catBooks[x]
                book_author = catBooks2[x]
                book_image = catimg[x][0]
                book_id = catid[x][0]

                cat_b_name = Label(cat_books_frame, text=f"{book_name}", font=('Microsoft YaHei UI Light', 12, 'bold'), bg="#FFCF96")
                cat_b_name.place(x=200, y=50)

                cat_b_author = Label(cat_books_frame, text=f"By {book_author}", font=('Microsoft YaHei UI Light', 12, 'bold'), bg="#FFCF96")
                cat_b_author.place(x=200, y=100)

                if book_image is not None:
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', mode='wb')
                    temp_file.write(book_image)
                    temp_file.close()

                    image = Image.open(temp_file.name)

                    Libbook_img = ImageTk.PhotoImage(image)
                    Libbook_lbl = Label(cat_books_frame)
                    Libbook_lbl.config(image=Libbook_img)
                    Libbook_lbl.image = Libbook_img
                    Libbook_lbl.place(x=50, y=50)

                else:
                    Libbook_lbl.config(image=None)

                Prev_button = Button(cat_books_frame, text="Preview", font=('Microsoft YaHei UI Light', 15), bg="#FF6969",
                                     fg="white", activebackground="#FF6969",command=lambda id=book_id: preview3(id))
                Prev_button.place(x=320, y=150)

                Pur_button = Button(cat_books_frame, text="Purchase", font=('Microsoft YaHei UI Light', 15), bg="#FF6969",
                                    fg="white", activebackground="#FF6969",command=lambda id=book_id: pur3(id))
                Pur_button.place(x=205, y=150)

                Pur_button = Button(cat_books_frame, text="Feedback", font=('Microsoft YaHei UI Light', 15), bg="grey",
                                    fg="white", activebackground="grey", command=feedback_frame)
                Pur_button.place(x=425, y=150)

        except Exception as e:
            print(e)


def back_btn_func():
    new_frame.place_forget()
    btn_frame.place_forget()

def on_configure9(event):
    lib_my_canvas.config(scrollregion=lib_my_canvas.bbox("all"))


def preview3(book_id):
    global Pre_frame2
    global Prev_back_img2
    global Bookimg_img
    global mycursor2
    global Libbook_lbl2
    global book_img2
    global Libbook_lbl3
    Pre_frame2 = Frame(new_frame, width=500, height=500, bg="white")
    Pre_frame2.place(x=280, y=20)

    Prev_back_img2 = PhotoImage(file="Assets//Back.png")
    Prev_Back_btn2 = Button(Pre_frame2, image=Prev_back_img2, command=back4, bg="white", border=0,
                            activebackground="white")
    Prev_Back_btn2.place(x=0, y=10)

    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor2 = con.cursor()

    except FileNotFoundError:
        messagebox.showerror("ERROR", "Connection Lost!!")

    query = "use library_books"
    mycursor2.execute(query)
    query2 = "select BookName from library where BookID=%s"
    mycursor2.execute(query2, (book_id))
    book_name = mycursor2.fetchone()
    query3 = "select BookAuthor from library where BookID=%s"
    mycursor2.execute(query3, (book_id))
    book_author_name = mycursor2.fetchone()
    query4 = "select BookInfo from library where BookID=%s"
    mycursor2.execute(query4, (book_id))
    book_info = mycursor2.fetchone()[0]
    query5 = "select BookImg from library where BookID=%s"
    mycursor2.execute(query5, (book_id))
    book_img2 = mycursor2.fetchone()[0]
    query6 = "select BookRating from library where BookID=%s"
    mycursor2.execute(query6, (book_id))
    book_rating = mycursor2.fetchone()[0]
    if book_img2 is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', mode='wb')
        temp_file.write(book_img2)
        temp_file.close()

        image2 = Image.open(temp_file.name)

        Libbook_img3 = ImageTk.PhotoImage(image2)
        Libbook_lbl3 = Label(Pre_frame2)
        Libbook_lbl3.config(image=Libbook_img3)
        Libbook_lbl3.image = Libbook_img3
        Libbook_lbl3.place(x=50, y=140)
    else:
        Libbook_lbl3.config(image=None)

    if book_name:
        Head2 = Label(Pre_frame2, text=book_name[0], font=("Microsoft YaHei UI Light", 20), bg="white")
        Head2.place(x=50, y=10)

        Author2 = Label(Pre_frame2, text=f"By {book_author_name[0]}", font=("Times", 15), bg="white")
        Author2.place(x=50, y=50)

        line2 = Frame(Pre_frame2, width=150, height=2, bg="blue")
        line2.place(x=50, y=80)

        Book_rating2 = Label(Pre_frame2, text=f"Rating: {book_rating} Stars", font=("Microsoft YaHei UI Light", 10),
                             bg="yellow")
        Book_rating2.place(x=50, y=410)

        Ab2 = Label(Pre_frame2, text="About:", font=("Microsoft YaHei UI Light", 20), bg="white")
        Ab2.place(x=280, y=80)

        About2 = Label(Pre_frame2, text=book_info, font=("Times", 10), bg="#F7E6C4", wraplength=200)
        About2.place(x=280, y=120)


def mail3():
    global userin
    global passin
    global pin_frame
    global Pur_back_img8
    global pin_input
    global num
    userin = username_input.get()
    passin = Password_input.get()

    if (userin == ""):
        messagebox.showerror("Error", "Username not Entered")

    elif (passin == ""):
        messagebox.showerror("Error", "Password not Entered")

    else:

        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor2 = con.cursor()
            query = "USE users"
            mycursor2.execute(query)

            query2 = "select username from userData where subscribe=0"
            mycursor2.execute(query2)
            subs = mycursor2.fetchone()

            query3 = "select Email from userData where username=%s"
            mycursor2.execute(query3, (userin))
            Email = mycursor2.fetchone()[0]

            if subs:
                random_number = random.randint(1000, 9999)
                num = str(random_number)
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("snapbooks9@gmail.com", "lrkprjqmofvxatjp")
                server.sendmail("snapbooks9@gmail.com", Email, num)

                messagebox.showinfo("Mail", "Mail sent on the required mail address!!")

                pur_frame2.place_forget()

                pin_frame = Frame(new_frame, width=400, height=300, bg="white")
                pin_frame.place(x=340, y=20)

                Pur_back_img8 = PhotoImage(file="Assets//Back.png")
                Pur_Back_btn8 = Button(pin_frame, image=Pur_back_img8, command=back8, bg="white", border=0,
                                      activebackground="white")
                Pur_Back_btn8.place(x=0, y=10)

                heading_lbl = Label(pin_frame, text="Pin Sent on Mail: ", font=("Roboto", 15), bg="white")
                heading_lbl.place(x=50, y=15)

                line_frame = Frame(pin_frame, width=300, height=2, bg="black")
                line_frame.place(x=50, y=45)

                pin_lbl = Label(pin_frame, text="Pincode", font=('Roboto', 15), bg="white")
                pin_lbl.place(x=50, y=100)

                pin_input = Entry(pin_frame)
                pin_input.place(x=200, y=100)

                Submit_pin = Button(pin_frame, text="Submit", bg='cyan', fg="black", font=("Roboto", 15), padx=100, command=execute3)
                Submit_pin.place(x=50, y=200)


            else:
                messagebox.showinfo("Info", "You are Already Subscribed!!")


        except Exception as e:
            print(e)


def execute3():
    pin_number = pin_input.get()

    if pin_number == num:
        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor2 = con.cursor()
            query = "USE users"
            mycursor2.execute(query)

            query2 = "update userdata set subscribe = 1 where username = %s"
            mycursor2.execute(query2, userin)
            con.commit()

            messagebox.showinfo("Subscribe", "You Are Subscribed!!")

        except EXCEPTION as e:
            print(e)

    else:
        messagebox.showerror("Error", "Invalid Pincode!!")



def back8():
    pin_frame.place_forget()

def pur3(book_id):
    global pur_frame2
    global Pur_back_img2
    global user2
    global username_input
    global Password_input
    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()
        query = "use users"
        mycursor.execute(query)
        query4 = "select username from userData where login_status=1 and subscribe=1"
        mycursor.execute(query4)
        user2 = mycursor.fetchone()

    except FileNotFoundError:
        messagebox.showerror("ERROR", "Connection Lost!!")

    if user2:
        try:
            con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
            mycursor = con.cursor()
            query = "use library_books"
            mycursor.execute(query)
            query2 = "select BookPdfs from library where BookID=%s"
            mycursor.execute(query2, (book_id))
            check4 = mycursor.fetchone()[0]
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
                temp_pdf_file.write(check4)
                temp_pdf_file_path = temp_pdf_file.name

            # Open the temporary PDF file in the default web browser
            wb.open(temp_pdf_file_path)

        except FileNotFoundError:
            messagebox.showerror("ERROR", "Connection Lost!!")

    elif not user2:
        pur_frame2 = Frame(new_frame, width=400, height=300, bg="white")
        pur_frame2.place(x=340, y=20)

        Pur_back_img2 = PhotoImage(file="Assets//Back.png")
        Pur_Back_btn = Button(pur_frame2, image=Pur_back_img2, command=back5, bg="white", border=0,
                              activebackground="white")
        Pur_Back_btn.place(x=0, y=10)

        heading_lbl = Label(pur_frame2, text="Subscribe: ", font=("Roboto", 15), bg="white")
        heading_lbl.place(x=50, y=15)

        line_frame = Frame(pur_frame2, width=300, height=2, bg="black")
        line_frame.place(x=50, y=45)

        username_lbl = Label(pur_frame2, text="Username", font=('Roboto', 15), bg="white")
        username_lbl.place(x=50, y=100)

        username_input = Entry(pur_frame2)
        username_input.place(x=200, y=100)

        Password_lbl = Label(pur_frame2, text="Password", font=('Roboto', 15), bg="white")
        Password_lbl.place(x=50, y=140)

        Password_input = Entry(pur_frame2)
        Password_input.place(x=200, y=140)

        Submit_btn = Button(pur_frame2, text="Submit", bg='cyan', fg="black", font=("Roboto", 15), padx=100,
                            command=mail3)
        Submit_btn.place(x=50, y=200)

def Search():
    global name
    searchin = search.get()

    try:
        con = pymysql.connect(host="localhost", user="root", password="Ajinkya@12")
        mycursor = con.cursor()
        query = "use library_books"
        mycursor.execute(query)

        query2 = "SELECT BookName From library WHERE BookName=%s"
        mycursor.execute(query2, searchin)
        name = mycursor.fetchone()[0]

        if searchin.lower() == name.lower():
            searchFrame = Frame(main_root, width=500, height=100, bg="white")
            searchFrame.place(x=190, y=51)

            BookLabel = Label(searchFrame, text=name, font=("Roboto", 20, "bold"), bg="white")
            BookLabel.place(x=30, y=0)

        else:
            searchFrame2 = Frame(main_root, width=500, height=100, bg="white")
            searchFrame2.place(x=190, y=51)

            BookLabel2 = Label(searchFrame2, text="None", font=("Roboto", 20, "bold"), bg="white")
            BookLabel2.place(x=30, y=0)
    except Exception as e:
        print(e)







def main():
    global Home_indicator
    global Library_indicator
    global main_root
    global home_frame1
    global search
    book_show_1_img = None
    main_root = Tk()
    main_root.title("Snapbooks")
    main_root.geometry("1290x1080")
    main_root.config(bg="white")

    # -------------Welcome Frame----------------#
    WelcomeFrame = Frame(main_root, width=1100, height=1080, bg="#E3F4F4")
    WelcomeFrame.place(x=190, y=51)

    book_img = PhotoImage(file="Assets//welcome Books.png")
    book_img_label = Label(WelcomeFrame, image=book_img, bg="#E3F4F4")
    book_img_label.place(x=0, y=100)

    welcome = Label(WelcomeFrame, text="Welcome to SnapBook an E-book App", font=('Roboto', 28), bg="#E3F4F4")
    welcome.place(x=400, y=200)

    welcome2 = Label(WelcomeFrame, text="Explore the Unknown", font=('Microsoft YaHei UI Light', 20), bg="#E3F4F4")
    welcome2.place(x=400, y=250)

    # -------------Steady Frame----------------#
    navbar_frame = Frame(main_root, width=1100, height=50, bg="white")
    navbar_frame.place(x=190, y=0)

    menu_frame = Frame(main_root, width=190, height=1080, bg="black")
    menu_frame.place(x=0, y=0)

    Home_btn = Button(menu_frame, text="Home", font=("Roboto", 25), border=0, bg="black", fg="#279EFF", activebackground="black", activeforeground="#279EFF", cursor="hand2", command=Hom_indicator)
    Home_btn.place(x=50, y=150)

    Home_img = PhotoImage(file="Assets//Home.png")
    Home_lbl = Label(menu_frame, image=Home_img, bg="black")
    Home_lbl.place(x=15, y=160)

    Home_indicator= Frame(menu_frame, bg="black", width=150, height=5)
    Home_indicator.place(x=19, y=200)

    Library_btn = Button(menu_frame, text="Library", font=("Roboto", 25), border=0, bg="black", fg="#279EFF", activebackground="black", activeforeground="#279EFF", cursor="hand2",
                      command=Lib_indicator)
    Library_btn.place(x=50, y=250)

    Library_img = PhotoImage(file="Assets//bookshelf.png")
    Library_lbl = Label(menu_frame, image=Library_img, bg="black")
    Library_lbl.place(x=15, y=260)

    Library_indicator= Frame(menu_frame, bg="black", width=150, height=5)
    Library_indicator.place(x=19, y=300)

    line = Frame(main_root, width=1100, height=1, bg="black")
    line.place(x=190, y=50)

    Book_img = PhotoImage(file="Assets//Book_app_name.png")
    Book_img_label = Label(menu_frame, image=Book_img, bg="black", border=0)
    Book_img_label.place(x=0, y=18)

    Book_name_line = Frame(menu_frame, width=190, height=2, bg="white")
    Book_name_line.place(x=0, y=70)

    Book_name = Label(menu_frame, text="SnapBook", border=0, bg="Black", font=("Microsoft YaHei UI Light", 22, "bold"), fg="#AED2FF")
    Book_name.place(x=35, y=18)

    feedback = Button(navbar_frame, text="Feedback", font=("Microsoft YaHei UI Light", 18), border=0, bg="white",
                      fg="black", cursor="hand2", command=feedback_frame, activebackground="white")
    feedback.place(x=890, y=1)

    search_img = PhotoImage(file="Assets//search.png")
    search_lbl = Button(navbar_frame, image=search_img, bg="white", command=Search)
    search_lbl.place(x=500, y=5)

    search = Entry(navbar_frame, font=("Microsoft YaHei UI Light", 15), border=2, width=35)
    search.place(x=100, y=10, height=35)
    search.insert(0, "Search Books")
    search.bind("<FocusIn>", on_enter)
    search.bind("<FocusOut>", on_leave)


    shop_img = PhotoImage(file="Assets//arrow.png")
    shop_btn = Button(navbar_frame, image=shop_img, bg="white", border=0, cursor="hand2", command=Logout)
    shop_btn.place(x=1030, y=4)

    main_root.mainloop()

if __name__ == '__main__':
    main()