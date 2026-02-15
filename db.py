import mysql.connector
from tkinter import messagebox

def connect_db():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="", 
            database="student_management" 
        )
        return con
    except mysql.connector.Error as err:
        if err.errno == 1049: # Database doesn't exist
            create_db()
            return connect_db()
        else:
            return None

def create_db():
    try:
        con = mysql.connector.connect(host="localhost", user="root", password="")
        cur = con.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS student_management")
        cur.execute("USE student_management")
        
        # Students Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no INT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                gender VARCHAR(10),
                dob DATE,
                contact VARCHAR(15),
                course VARCHAR(50),
                address TEXT
            )
        """)
        
        # Results Table (Linked via Foreign Key)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                roll_no INT,
                name VARCHAR(100),
                course VARCHAR(50),
                marks_ob INT,
                full_marks INT,
                percentage FLOAT,
                FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
            )
        """)
        con.commit()
        con.close()
    except Exception as e:
        print(f"Init Error: {e}")

if __name__ == "__main__":
    create_db()