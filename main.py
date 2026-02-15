from tkinter import *
from tkinter import messagebox
from student import Student
from result import Result
from db import connect_db

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # Title
        title = Label(self.root, text="Student Result Management System", bd=10, relief=GROOVE, font=("times new roman", 40, "bold"), bg="navy", fg="white")
        title.pack(side=TOP, fill=X)

        # Menu Frame (can use Menu or just buttons)
        # For simplicity and robust UI, using Buttons on the side or top
        
        # Heading
        Label(self.root, text="Dashboard", font=("times new roman", 20, "bold"), bg="white").place(x=10, y=80)
        
        # Buttons
        btn_student = Button(self.root, text="Student Details", command=self.student_details, font=("times new roman", 15, "bold"), bg="crimson", fg="white", cursor="hand2")
        btn_student.place(x=100, y=150, width=220, height=40)

        btn_result = Button(self.root, text="Result Details", command=self.result_details, font=("times new roman", 15, "bold"), bg="crimson", fg="white", cursor="hand2")
        btn_result.place(x=400, y=150, width=220, height=40)
        
        btn_exit = Button(self.root, text="Exit", command=self.root.quit, font=("times new roman", 15, "bold"), bg="red", fg="white", cursor="hand2")
        btn_exit.place(x=700, y=150, width=220, height=40)

        # Content / Cards
        self.lbl_student = Label(self.root, text="Total Students\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#e1f5fe", fg="#0277bd")
        self.lbl_student.place(x=200, y=300, width=300, height=100)

        self.lbl_result = Label(self.root, text="Total Results\n[ 0 ]", font=("goudy old style", 20), bd=10, relief=RIDGE, bg="#fce4ec", fg="#e91e63")
        self.lbl_result.place(x=600, y=300, width=300, height=100)

        # Footer
        footer = Label(self.root, text="SRMS - Student Result Management System\nDeveloped By Antigravity", font=("times new roman", 12), bg="#262626", fg="white")
        footer.pack(side=BOTTOM, fill=X)

        self.update_details()

    def update_details(self):
        con = connect_db()
        cur = con.cursor()
        try:
            cur.execute("select * from students")
            cr = cur.fetchall()
            self.lbl_student.config(text=f"Total Students\n[ {str(len(cr))} ]")

            cur.execute("select * from results")
            cr = cur.fetchall()
            self.lbl_result.config(text=f"Total Results\n[ {str(len(cr))} ]")
            
            self.root.after(5000, self.update_details) # Auto refresh every 5 seconds
        except Exception as ex:
             # If DB error, just ignore or log to console, don't popup every 5s
             print(f"Error updating details: {ex}")
        finally:
            con.close()

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def result_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Result(self.new_window)

if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()
