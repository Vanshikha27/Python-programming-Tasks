from tkinter import *
import tkinter.messagebox as tkMessageBox
from tkinter import messagebox
import sqlite3

root = Tk()
root.title("Student Database")
 
width = 640
height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `student` (stud_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,stud_name TEXT, stud_subject text, stud_marks int)")

USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()


def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=80)
    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = Label(LoginFrame, text="Don't Have an Account? Register", fg="Blue", font=('arial', 12))
    lbl_register.grid(row=7, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)
 
def RegisterForm():
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(root)
    RegisterFrame.pack(side=TOP, pady=40)
    lbl_username = Label(RegisterFrame, text="Username:", font=('arial', 18), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18)
    lbl_password.grid(row=2)
    lbl_firstname = Label(RegisterFrame, text="Firstname:", font=('arial', 18), bd=18)
    lbl_firstname.grid(row=3)
    lbl_lastname = Label(RegisterFrame, text="Lastname:", font=('arial', 18), bd=18)
    lbl_lastname.grid(row=4)
    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=5, columnspan=2)
    username = Entry(RegisterFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=3, column=1)
    lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=LASTNAME, width=15)
    lastname.grid(row=4, column=1)
    btn_login = Button(RegisterFrame, text="Register", font=('arial', 18), width=35, command=Register)
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(RegisterFrame, text="Already have an account : Login", fg="Blue", font=('arial', 12))
    lbl_login.grid(row=7, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()
 
def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()

def Register():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO `member` (username, password, firstname, lastname) VALUES(?, ?, ?, ?)", (str(USERNAME.get()), str(PASSWORD.get()), str(FIRSTNAME.get()), str(LASTNAME.get())))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            FIRSTNAME.set("")
            LASTNAME.set("")
            lbl_result2.config(text="Successfully Created!", fg="black")
        cursor.close()
        conn.close()
def Login():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="blue")
            LoginFrame.destroy()
            StudentForm()
        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")

stud_name = StringVar()
stud_subject=StringVar()
stud_marks=StringVar()

def StudentForm():
    global StudentFrame, lbl_result3
    StudentFrame = Frame(root)
    StudentFrame.pack(side=TOP, pady=40)
    lbl_stud_name = Label(StudentFrame , text="Student Name:", font=('arial', 18), bd=18)
    lbl_stud_name.grid(row=1)
    lbl_stud_subject = Label(StudentFrame , text="Student Subject:", font=('arial', 18), bd=18)
    lbl_stud_subject.grid(row=2)
    lbl_stud_marks = Label(StudentFrame , text="Student Marks:", font=('arial', 18), bd=18)
    lbl_stud_marks.grid(row=3)
    lbl_result3 = Label(StudentFrame , text="", font=('arial', 18))
    lbl_result3.grid(row=5, columnspan=2)
    name = Entry(StudentFrame , font=('arial', 20), textvariable=stud_name, width=15)
    name.grid(row=1, column=1)
    subject = Entry(StudentFrame, font=('arial', 20), textvariable=stud_subject, width=15)
    subject.grid(row=2, column=1)
    marks = Entry(StudentFrame, font=('arial', 20), textvariable=stud_marks, width=15)
    marks.grid(row=3, column=1)
    btn_add = Button(StudentFrame, text="ADD", font=('arial', 18), width=35, command=add)
    btn_add.grid(row=6, columnspan=2, pady=20)
    lbl_search = Label(StudentFrame, text="You can search", fg="Blue", font=('arial', 12))
    lbl_search.grid(row=7, sticky=W)
    lbl_search.bind('<Button-1>', ToggleToSearch)

def to_Search():
    global SFrame ,lbl_result4
    SFrame= Frame(root)
    SFrame.pack(side=TOP,pady=40)
    lbl_stud_name = Label(SFrame , text="Student Name:", font=('arial', 18), bd=18)
    lbl_stud_name.grid(row=1)
    lbl_result4 = Label(SFrame , text="", font=('arial', 18))
    lbl_result4.grid(row=2, columnspan=2)
    name = Entry(SFrame , font=('arial', 20), textvariable=stud_name, width=15)
    name.grid(row=1, column=1)
    btn_search = Button(SFrame, text="SEARCH ID", font=('arial', 18), width=35, command=searchid)
    btn_search.grid(row=3, columnspan=2, pady=20)
    btn_search = Button(SFrame, text="SEARCH Subjects", font=('arial', 18), width=35, command=searchsubject)
    btn_search.grid(row=4, columnspan=2, pady=20)
    btn_search = Button(SFrame, text="SEARCH Marks", font=('arial', 18), width=35, command=searchmarks)
    btn_search.grid(row=5,columnspan=2, pady=20)
    lbl_add = Label(SFrame, text="You can add a record", fg="Blue", font=('arial', 12))
    lbl_add.grid(row=6, sticky=W)
    lbl_add.bind('<Button-1>', ToggleToAdd)
    

def ToggleToSearch(event=None):
    StudentFrame.destroy()
    to_Search()

def ToggleToAdd(event=None):
    SFrame.destroy()
    StudentForm()

def add():
    Database()
    if stud_name.get == "" or stud_subject.get() == "" or stud_marks.get() == "" :
        lbl_result3.config(text="Please complete the required field!", fg="orange")
    else:
    
        if cursor.fetchone() is not None:
            lbl_result3.config(text="Record is already there", fg="red")
        else:
            cursor.execute("INSERT INTO `student` (stud_name, stud_subject, stud_marks) VALUES(?, ?, ?)", (str(stud_name.get()), str(stud_subject.get()), str(stud_marks.get())))
            conn.commit()
            stud_name.set("")
            stud_subject.set("")
            stud_marks.set("")
            
            lbl_result3.config(text="Successfully Added!", fg="black")
        cursor.close()
        conn.close()

def searchid():
    Database()
    el=[]
    with conn:
        cursor = conn.cursor()
        cursor.execute('select * from student where stud_name=?',(stud_name.get(),))
        record = cursor.fetchall()
        if record == el:
            messagebox.showinfo("Record not found!",(stud_name.get() ,' has not yet registered!'))
        else:
            for row in record:
                stud_id= row[0]
                messagebox.showinfo("Student Details Found",('Student ID: ',stud_id ))

def searchsubject():
    Database()
    el=[]
    with conn:
        cursor = conn.cursor()
        cursor.execute('select * from student where stud_name=?',(stud_name.get(),))
        record = cursor.fetchall()
        if record == el:
            messagebox.showinfo("Record not found!",(stud_name.get() ,' has not yet registered!'))
        else:
            for row in record:
                stud_subject = row[2]
                messagebox.showinfo("Student Details Found",('Student Subject: ',stud_subject))

def searchmarks():
    Database()
    el=[]
    with conn:
        cursor = conn.cursor()
        cursor.execute('select * from student where stud_name=?',(stud_name.get(),))
        record = cursor.fetchall()
        if record == el:
            messagebox.showinfo("Record not found!",(stud_name.get() ,' has not yet registered!'))
        else:
            for row in record:
                stud_marks = row [3]
                messagebox.showinfo("Student Details Found",('Student Marks: ',stud_marks))
    

LoginForm()

if __name__ == '__main__':
    root.mainloop()