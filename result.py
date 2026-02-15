from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from db import connect_db

class Result:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")

        title = Label(self.root, text="Manage Student Results", bd=10, relief=GROOVE, font=("times new roman", 40, "bold"), bg="orange", fg="white")
        title.pack(side=TOP, fill=X)

        # Variables
        self.roll_no_var = StringVar()
        self.name_var = StringVar()
        self.course_var = StringVar()
        self.marks_var = StringVar()
        self.full_marks_var = StringVar()

        # Manage Frame
        Manage_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Manage_Frame.place(x=20, y=100, width=450, height=580)

        m_title = Label(Manage_Frame, text="Add Result", bg="white", fg="black", font=("times new roman", 30, "bold"))
        m_title.grid(row=0, columnspan=2, pady=20)

        lbl_roll = Label(Manage_Frame, text="Roll No.", bg="white", font=("times new roman", 20, "bold"))
        lbl_roll.grid(row=1, column=0, pady=10, sticky="w", padx=20)
        txt_roll = Entry(Manage_Frame, textvariable=self.roll_no_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_roll.grid(row=1, column=1, pady=10, sticky="w", padx=20)
        
        btn_search = Button(Manage_Frame, text="Search", command=self.search_student, width=10, bg="blue", fg="white", font=("times new roman", 10, "bold")).grid(row=1, column=2, padx=10)


        lbl_name = Label(Manage_Frame, text="Name", bg="white", font=("times new roman", 20, "bold"))
        lbl_name.grid(row=2, column=0, pady=10, sticky="w", padx=20)
        txt_name = Entry(Manage_Frame, textvariable=self.name_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE, state='readonly')
        txt_name.grid(row=2, column=1, pady=10, sticky="w", padx=20)

        lbl_course = Label(Manage_Frame, text="Course", bg="white", font=("times new roman", 20, "bold"))
        lbl_course.grid(row=3, column=0, pady=10, sticky="w", padx=20)
        txt_course = Entry(Manage_Frame, textvariable=self.course_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE, state='readonly')
        txt_course.grid(row=3, column=1, pady=10, sticky="w", padx=20)

        lbl_marks = Label(Manage_Frame, text="Marks Obtained", bg="white", font=("times new roman", 20, "bold"))
        lbl_marks.grid(row=4, column=0, pady=10, sticky="w", padx=20)
        txt_marks = Entry(Manage_Frame, textvariable=self.marks_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_marks.grid(row=4, column=1, pady=10, sticky="w", padx=20)

        lbl_full_marks = Label(Manage_Frame, text="Full Marks", bg="white", font=("times new roman", 20, "bold"))
        lbl_full_marks.grid(row=5, column=0, pady=10, sticky="w", padx=20)
        txt_full_marks = Entry(Manage_Frame, textvariable=self.full_marks_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_full_marks.grid(row=5, column=1, pady=10, sticky="w", padx=20)

        # Buttons
        btn_Frame = Frame(Manage_Frame, bd=4, relief=RIDGE, bg="white")
        btn_Frame.place(x=15, y=500, width=420)

        Addbtn = Button(btn_Frame, text="Submit", width=15, command=self.add_result, bg="green", fg="white", font=("times new roman", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
        Clearbtn = Button(btn_Frame, text="Clear", width=15, command=self.clear, bg="gray", fg="white", font=("times new roman", 12, "bold")).grid(row=0, column=1, padx=10, pady=10)

        # Result Table
        Table_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Table_Frame.place(x=500, y=100, width=800, height=580)
        
        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.Result_Table = ttk.Treeview(Table_Frame, columns=("id", "roll", "name", "course", "marks", "full", "per"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Result_Table.xview)
        scroll_y.config(command=self.Result_Table.yview)

        self.Result_Table.heading("id", text="ID")
        self.Result_Table.heading("roll", text="Roll No")
        self.Result_Table.heading("name", text="Name")
        self.Result_Table.heading("course", text="Course")
        self.Result_Table.heading("marks", text="Marks Obt")
        self.Result_Table.heading("full", text="Full Marks")
        self.Result_Table.heading("per", text="Percentage")

        self.Result_Table['show'] = 'headings'
        self.Result_Table.column("id", width=50)
        self.Result_Table.column("roll", width=100)
        self.Result_Table.column("name", width=150)
        self.Result_Table.column("course", width=100)
        self.Result_Table.column("marks", width=100)
        self.Result_Table.column("full", width=100)
        self.Result_Table.column("per", width=100)

        self.Result_Table.pack(fill=BOTH, expand=1)
        self.fetch_data()

    def search_student(self):
        con = connect_db()
        cur = con.cursor()
        try:
            cur.execute("select name, course from students where roll_no=%s", (self.roll_no_var.get(),))
            row = cur.fetchone()
            if row:
                self.name_var.set(row[0])
                self.course_var.set(row[1] if row[1] else "N/A")
            else:
                 messagebox.showerror("Error", "No record found")
        except mysql.connector.Error as err:
             messagebox.showerror("Error", f"Error due to : {str(err)}")
        finally:
            con.close()

    def add_result(self):
        if self.roll_no_var.get() == "" or self.marks_var.get() == "":
             messagebox.showerror("Error", "Please search student and enter marks")
        else:
            con = connect_db()
            cur = con.cursor()
            try:
                per = (int(self.marks_var.get()) * 100) / int(self.full_marks_var.get())
                cur.execute("insert into results (roll_no, name, course, marks_ob, full_marks, percentage) values(%s, %s, %s, %s, %s, %s)",
                               (self.roll_no_var.get(),
                                self.name_var.get(),
                                self.course_var.get(),
                                self.marks_var.get(),
                                self.full_marks_var.get(),
                                str(per)
                               ))
                con.commit()
                self.fetch_data()
                self.clear()
                messagebox.showinfo("Success", "Result Added Successfully")
            except mysql.connector.Error as err:
                 messagebox.showerror("Error", f"Error due to : {str(err)}")
            finally:
                con.close()

    def fetch_data(self):
        con = connect_db()
        cur = con.cursor()
        cur.execute("select * from results")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Result_Table.delete(*self.Result_Table.get_children())
            for row in rows:
                self.Result_Table.insert('', END, values=row)
        con.close()

    def clear(self):
        self.roll_no_var.set("")
        self.name_var.set("")
        self.course_var.set("")
        self.marks_var.set("")
        self.full_marks_var.set("")

if __name__ == "__main__":
    root = Tk()
    obj = Result(root)
    root.mainloop()
