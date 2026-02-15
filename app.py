from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from db import connect_db

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

@app.route('/')
def index():
    con = connect_db()
    if not con:
        flash("Database connection failed!", "danger")
        return render_template('index.html', total_students=0, total_results=0)
    
    cur = con.cursor()
    
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM results")
    total_results = cur.fetchone()[0]
    
    con.close()
    return render_template('index.html', total_students=total_students, total_results=total_results)

@app.route('/students', methods=['GET', 'POST'])
def students():
    con = connect_db()
    cur = con.cursor()
    
    if request.method == 'POST':
        if 'add' in request.form:
            try:
                roll_no = request.form['roll_no']
                name = request.form['name']
                email = request.form['email']
                gender = request.form['gender']
                dob = request.form['dob']
                course = request.form['course']
                contact = request.form['contact']
                address = request.form['address']
                
                cur.execute("INSERT INTO students (roll_no, name, email, gender, dob, course, contact, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (roll_no, name, email, gender, dob, course, contact, address))
                con.commit()
                flash("Student added successfully!", "success")
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
        
        elif 'update' in request.form:
            try:
                roll_no = request.form['roll_no']
                name = request.form['name']
                email = request.form['email']
                gender = request.form['gender']
                dob = request.form['dob']
                course = request.form['course']
                contact = request.form['contact']
                address = request.form['address']

                cur.execute("UPDATE students SET name=%s, email=%s, gender=%s, dob=%s, course=%s, contact=%s, address=%s WHERE roll_no=%s",
                            (name, email, gender, dob, course, contact, address, roll_no))
                con.commit()
                flash("Student updated successfully!", "success")
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
        
        elif 'delete' in request.form:
             try:
                roll_no = request.form['roll_no']
                cur.execute("DELETE FROM students WHERE roll_no=%s", (roll_no,))
                con.commit()
                flash("Student deleted successfully!", "success")
             except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
                
        return redirect(url_for('students'))

    # Fetch all students
    search_query = request.args.get('search', '')
    if search_query:
        cur.execute(f"SELECT * FROM students WHERE name LIKE '%{search_query}%' OR roll_no LIKE '%{search_query}%'")
    else:
        cur.execute("SELECT * FROM students")
    
    students_data = cur.fetchall()
    con.close()
    return render_template('students.html', students=students_data)

@app.route('/results', methods=['GET', 'POST'])
def results():
    con = connect_db()
    cur = con.cursor()

    if request.method == 'POST':
        if 'add' in request.form:
            try:
                roll_no = request.form['roll_no']
                
                # Fetch student name and course automatically if possible, or just validate roll_no exists
                cur.execute("SELECT name, course FROM students WHERE roll_no=%s", (roll_no,))
                student = cur.fetchone()
                
                if student:
                    name = student[0]
                    course = student[1]
                    marks_ob = int(request.form['marks_ob'])
                    full_marks = int(request.form['full_marks'])
                    percentage = (marks_ob * 100) / full_marks
                    
                    cur.execute("INSERT INTO results (roll_no, name, course, marks_ob, full_marks, percentage) VALUES (%s, %s, %s, %s, %s, %s)",
                                (roll_no, name, course, marks_ob, full_marks, percentage))
                    con.commit()
                    flash("Result added successfully!", "success")
                else:
                    flash("Student not found! Please check Roll No.", "danger")
            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
        
        elif 'delete' in request.form:
             try:
                result_id = request.form['id']
                cur.execute("DELETE FROM results WHERE id=%s", (result_id,))
                con.commit()
                flash("Result deleted successfully!", "success")
             except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")

        return redirect(url_for('results'))

    # Fetch all results
    cur.execute("SELECT * FROM results")
    results_data = cur.fetchall()
    con.close()
    return render_template('results.html', results=results_data)

if __name__ == '__main__':
    app.run(debug=True)
