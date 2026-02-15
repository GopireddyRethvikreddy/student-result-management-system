from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from db import connect_db

class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1350x700+0+0")

        title = Label(self.root, text="Manage Student Details", bd=10, relief=GROOVE, font=("times new roman", 40, "bold"), bg="yellow", fg="red")
        title.pack(side=TOP, fill=X)

        # Variables
        self.Roll_No_var = StringVar()
        self.Name_var = StringVar()
        self.Email_var = StringVar()
        self.Gender_var = StringVar()
        self.Dob_var = StringVar()
        self.Contact_var = StringVar()
        self.Course_var = StringVar()
        
        self.search_by = StringVar()
        self.search_txt = StringVar()

        # Manage Frame
        Manage_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        Manage_Frame.place(x=20, y=100, width=450, height=580)

        m_title = Label(Manage_Frame, text="Manage Students", bg="crimson", fg="white", font=("times new roman", 30, "bold"))
        m_title.grid(row=0, columnspan=2, pady=20)

        lbl_roll = Label(Manage_Frame, text="Roll No.", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_roll.grid(row=1, column=0, pady=10, sticky="w", padx=10)
        txt_roll = Entry(Manage_Frame, textvariable=self.Roll_No_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_roll.grid(row=1, column=1, pady=10, sticky="w", padx=10)

        lbl_name = Label(Manage_Frame, text="Name", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_name.grid(row=2, column=0, pady=10, sticky="w", padx=10)
        txt_name = Entry(Manage_Frame, textvariable=self.Name_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_name.grid(row=2, column=1, pady=10, sticky="w", padx=10)

        lbl_email = Label(Manage_Frame, text="Email", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_email.grid(row=3, column=0, pady=10, sticky="w", padx=10)
        txt_email = Entry(Manage_Frame, textvariable=self.Email_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_email.grid(row=3, column=1, pady=10, sticky="w", padx=10)

        lbl_gender = Label(Manage_Frame, text="Gender", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_gender.grid(row=4, column=0, pady=10, sticky="w", padx=10)
        combo_gender = ttk.Combobox(Manage_Frame, textvariable=self.Gender_var, font=("times new roman", 13, "bold"), state='readonly')
        combo_gender['values'] = ("Male", "Female", "Other")
        combo_gender.grid(row=4, column=1, pady=10, sticky="w", padx=10)

        lbl_dob = Label(Manage_Frame, text="D.O.B", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_dob.grid(row=5, column=0, pady=10, sticky="w", padx=10)
        txt_dob = Entry(Manage_Frame, textvariable=self.Dob_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_dob.grid(row=5, column=1, pady=10, sticky="w", padx=10)

        lbl_course = Label(Manage_Frame, text="Course", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_course.grid(row=6, column=0, pady=10, sticky="w", padx=10)
        txt_course = Entry(Manage_Frame, textvariable=self.Course_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_course.grid(row=6, column=1, pady=10, sticky="w", padx=10)

        lbl_contact = Label(Manage_Frame, text="Contact", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_contact.grid(row=7, column=0, pady=10, sticky="w", padx=10)
        txt_contact = Entry(Manage_Frame, textvariable=self.Contact_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_contact.grid(row=7, column=1, pady=10, sticky="w", padx=10)

        lbl_address = Label(Manage_Frame, text="Address", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_address.grid(row=8, column=0, pady=10, sticky="w", padx=10)
        self.txt_address = Text(Manage_Frame, width=25, height=3, font=("times new roman", 10))
        self.txt_address.grid(row=8, column=1, pady=10, sticky="w", padx=10)

        # Button Frame
        btn_Frame = Frame(Manage_Frame, bd=4, relief=RIDGE, bg="crimson")
        btn_Frame.place(x=10, y=520, width=420)

        Addbtn = Button(btn_Frame, text="Add", width=10, command=self.add_student).grid(row=0, column=0, padx=5, pady=5)
        Updatebtn = Button(btn_Frame, text="Update", width=10, command=self.update_student).grid(row=0, column=1, padx=5, pady=5)
        Deletebtn = Button(btn_Frame, text="Delete", width=10, command=self.delete_student).grid(row=0, column=2, padx=5, pady=5)
        Clearbtn = Button(btn_Frame, text="Clear", width=10, command=self.clear).grid(row=0, column=3, padx=5, pady=5)

        # Detail Frame
        Detail_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="crimson")
        Detail_Frame.place(x=500, y=100, width=800, height=580)

        lbl_search = Label(Detail_Frame, text="Search By", bg="crimson", fg="white", font=("times new roman", 20, "bold"))
        lbl_search.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        combo_search = ttk.Combobox(Detail_Frame, textvariable=self.search_by, width=10, font=("times new roman", 13, "bold"), state='readonly')
        combo_search['values'] = ("Roll_No", "Name", "Contact")
        combo_search.grid(row=0, column=1, padx=20, pady=10)

        txt_search = Entry(Detail_Frame, textvariable=self.search_txt, width=20, font=("times new roman", 10, "bold"), bd=5, relief=GROOVE)
        txt_search.grid(row=0, column=2, padx=20, pady=10)

        searchbtn = Button(Detail_Frame, text="Search", width=10, pady=5, command=self.search_data).grid(row=0, column=3, padx=10, pady=10)
        showallbtn = Button(Detail_Frame, text="Show All", width=10, pady=5, command=self.fetch_data).grid(row=0, column=4, padx=10, pady=10)

        # Table Frame
        Table_Frame = Frame(Detail_Frame, bd=4, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=10, y=70, width=760, height=500)

        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.Student_Table = ttk.Treeview(Table_Frame, columns=("roll", "name", "email", "gender", "dob", "course", "contact", "address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Student_Table.xview)
        scroll_y.config(command=self.Student_Table.yview)

        self.Student_Table.heading("roll", text="Roll No.")
        self.Student_Table.heading("name", text="Name")
        self.Student_Table.heading("email", text="Email")
        self.Student_Table.heading("gender", text="Gender")
        self.Student_Table.heading("dob", text="D.O.B")
        self.Student_Table.heading("course", text="Course")
        self.Student_Table.heading("contact", text="Contact")
        self.Student_Table.heading("address", text="Address")

        self.Student_Table['show'] = 'headings'
        self.Student_Table.column("roll", width=80)
        self.Student_Table.column("name", width=100)
        self.Student_Table.column("email", width=100)
        self.Student_Table.column("gender", width=80)
        self.Student_Table.column("dob", width=80)
        self.Student_Table.column("course", width=80)
        self.Student_Table.column("contact", width=100)
        self.Student_Table.column("address", width=120)

        self.Student_Table.pack(fill=BOTH, expand=1)
        self.Student_Table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()

    def add_student(self):
        if self.Roll_No_var.get() == "" or self.Name_var.get() == "":
             messagebox.showerror("Error", "All fields are required")
        else:
            con = connect_db()
            cur = con.cursor()
            try:
                cur.execute("insert into students (roll_no, name, email, gender, dob, course, contact, address) values(%s, %s, %s, %s, %s, %s, %s, %s)",
                               (self.Roll_No_var.get(),
                                self.Name_var.get(),
                                self.Email_var.get(),
                                self.Gender_var.get(),
                                self.Dob_var.get(),
                                self.Course_var.get(),
                                self.Contact_var.get(),
                                self.txt_address.get('1.0', END)
                               ))
                con.commit()
                self.fetch_data()
                self.clear()
                con.close()
                messagebox.showinfo("Success", "Record has been inserted")
            except mysql.connector.Error as err:
                 messagebox.showerror("Error", f"Error due to : {str(err)}")

    def fetch_data(self):
        con = connect_db()
        cur = con.cursor()
        cur.execute("select * from students")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Student_Table.delete(*self.Student_Table.get_children())
            for row in rows:
                # db structure: roll_no(0), name(1), email(2), gender(3), dob(4), contact(5), admission(6), course(7), ... address(11)
                # We need to map correctly. 
                # Let's select specific columns to be safe or rely on index.
                # db.py: 
                # 0: roll_no, 1: name, 2: email, 3: gender, 4: dob, 5: contact, 6: admission_date, 7: course, 8: state, 9: city, 10: pin, 11: address
                row_data = (row[0], row[1], row[2], row[3], row[4], row[7], row[5], row[11])
                self.Student_Table.insert('', END, values=row_data)
        con.close()

    def clear(self):
        self.Roll_No_var.set("")
        self.Name_var.set("")
        self.Email_var.set("")
        self.Gender_var.set("")
        self.Dob_var.set("")
        self.Course_var.set("")
        self.Contact_var.set("")
        self.txt_address.delete("1.0", END)

    def get_cursor(self, ev):
        cursor_row = self.Student_Table.focus()
        contents = self.Student_Table.item(cursor_row)
        row = contents['values']
        if row:
            self.Roll_No_var.set(row[0])
            self.Name_var.set(row[1])
            self.Email_var.set(row[2])
            self.Gender_var.set(row[3])
            self.Dob_var.set(row[4])
            self.Course_var.set(row[5])
            self.Contact_var.set(row[6])
            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, row[7])

    def update_student(self):
        con = connect_db()
        cur = con.cursor()
        try:
            cur.execute("update students set name=%s, email=%s, gender=%s, dob=%s, course=%s, contact=%s, address=%s where roll_no=%s",
                           (self.Name_var.get(),
                            self.Email_var.get(),
                            self.Gender_var.get(),
                            self.Dob_var.get(),
                            self.Course_var.get(),
                            self.Contact_var.get(),
                            self.txt_address.get('1.0', END),
                            self.Roll_No_var.get()
                           ))
            con.commit()
            self.fetch_data()
            self.clear()
            con.close()
            messagebox.showinfo("Success", "Record has been updated")
        except mysql.connector.Error as err:
             messagebox.showerror("Error", f"Error due to : {str(err)}")

    def delete_student(self):
        con = connect_db()
        cur = con.cursor()
        try:
            cur.execute("delete from students where roll_no=%s", (self.Roll_No_var.get(),))
            con.commit()
            con.close()
            self.fetch_data()
            self.clear()
            messagebox.showinfo("Success", "Record has been deleted")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error due to : {str(err)}")

    def search_data(self):
        con = connect_db()
        cur = con.cursor()
        try:
            cur.execute("select * from students where " + str(self.search_by.get()) + " LIKE '%" + str(self.search_txt.get()) + "%'")
            rows = cur.fetchall()
            if len(rows) != 0:
                self.Student_Table.delete(*self.Student_Table.get_children())
                for row in rows:
                     row_data = (row[0], row[1], row[2], row[3], row[4], row[7], row[5], row[11])
                     self.Student_Table.insert('', END, values=row_data)
            con.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error due to : {str(err)}")

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
