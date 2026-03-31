from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('students.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 age INTEGER,
                 course TEXT)''')
    conn.close()

init_db()

# Home Page
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('students.db')

    if request.method == 'POST':
        search = request.form['search']
        students = conn.execute("SELECT * FROM students WHERE name LIKE ?", 
                                ('%' + search + '%',)).fetchall()
    else:
        students = conn.execute('SELECT * FROM students').fetchall()

    conn.close()
    return render_template('index.html', students=students)
# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        conn = sqlite3.connect('students.db')
        conn.execute('INSERT INTO students (name, age, course) VALUES (?, ?, ?)',
                     (name, age, course))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

# Delete Student
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('students.db')
    conn.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Edit Student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('students.db')

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        conn.execute('UPDATE students SET name=?, age=?, course=? WHERE id=?',
                     (name, age, course, id))
        conn.commit()
        conn.close()
        return redirect('/')

    student = conn.execute('SELECT * FROM students WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', student=student)
app.run(debug=True)