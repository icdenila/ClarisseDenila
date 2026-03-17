from flask import Flask, jsonify, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# Creates 'students.db' in the same folder as this script
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)

# Create the database file and tables automatically
with app.app_context():
    db.create_all()

# Helper function for logic
def get_remarks(grade):
    return "Pass" if grade >= 75 else "Fail"

# --- ROUTES ---

@app.route('/')
def home():
    html = """
    <h1>Student API Dashboard</h1>
    <nav>
        <a href="/students">View Students</a> | 
        <a href="/add_student_form">Add Student</a> | 
        <a href="/summary">View JSON Summary</a>
    </nav>
    """
    return render_template_string(html)

@app.route('/students')
def list_students():
    # Fetch all records from the database
    all_students = Student.query.all()
    
    html = """
    <h2>Student List</h2>
    <table border="1" cellpadding="10" style="border-collapse: collapse;">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Grade</th>
            <th>Section</th>
            <th>Remarks</th>
            <th>Actions</th>
        </tr>
        {% for s in students %}
        <tr>
            <td>{{ s.id }}</td>
            <td>{{ s.name }}</td>
            <td>{{ s.grade }}</td>
            <td>{{ s.section }}</td>
            <td>{{ get_remarks(s.grade) }}</td>
            <td>
                <a href="/delete/{{ s.id }}" onclick="return confirm('Delete this student?')">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    <br><a href="/">Back to Home</a>
    """
    return render_template_string(html, students=all_students, get_remarks=get_remarks)

@app.route('/add_student_form')
def add_student_form():
    html = """
    <h2>Add New Student</h2>
    <form action="/add_student" method="POST">
        <label>Name:</label><br>
        <input type="text" name="name" required><br><br>
        
        <label>Grade:</label><br>
        <input type="number" name="grade" min="0" max="100" required><br><br>
        
        <label>Section:</label><br>
        <input type="text" name="section" required><br><br>
        
        <button type="submit">Save Student</button>
    </form>
    <br><a href="/">Back</a>
    """
    return render_template_string(html)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")

    # Insert into Database
    new_student = Student(name=name, grade=grade, section=section)
    db.session.add(new_student)
    db.session.commit()

    return redirect(url_for('list_students'))

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('list_students'))

@app.route('/summary')
def summary():
    all_students = Student.query.all()
    if not all_students:
        return jsonify({"error": "No data available"}), 404

    grades = [s.grade for s in all_students]
    passed = len([g for g in grades if g >= 75])
    failed = len(grades) - passed
    avg = sum(grades) / len(grades)

    return jsonify({
        "total_students": len(all_students),
        "average_grade": round(avg, 2),
        "passed": passed,
        "failed": failed
    })

if __name__ == '__main__':
    app.run(debug=True)
