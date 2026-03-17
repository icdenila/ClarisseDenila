from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Temporary database (list)
students = [
    {"id": 1, "name": "Ic Denila", "grade": 90, "section": "Android"},
    {"id": 2, "name": "Mona Mae Calubia", "grade": 95, "section": "Arduino"},
    {"id": 3, "name": "Annie Franco", "grade": 70, "section": "Android"}
]

# Function to check pass/fail
def remarks(grade):
    return "Pass" if grade >= 75 else "Fail"


# HOME PAGE
@app.route('/')
def home():
    html = """
    <h1>Student API Dashboard</h1>

    <a href="/students">View Students</a><br><br>
    <a href="/add_student_form">Add Student</a><br><br>
    <a href="/summary">View Summary</a>
    """
    return render_template_string(html)


# VIEW ALL STUDENTS
@app.route('/students')
def list_students():

    html = """
    <h2>Student List</h2>

    <table border="1" cellpadding="10">
    <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Grade</th>
        <th>Section</th>
        <th>Remarks</th>
    </tr>

    {% for s in students %}
    <tr>
        <td>{{s.id}}</td>
        <td>{{s.name}}</td>
        <td>{{s.grade}}</td>
        <td>{{s.section}}</td>
        <td>{{remarks(s.grade)}}</td>
    </tr>
    {% endfor %}
    </table>

    <br>
    <a href="/">Back</a>
    """

    return render_template_string(html, students=students, remarks=remarks)


# FORM TO ADD STUDENT
@app.route('/add_student_form')
def add_student_form():

    html = """
    <h2>Add Student</h2>

    <form action="/add_student" method="POST">

    Name:<br>
    <input type="text" name="name"><br><br>

    Grade:<br>
    <input type="number" name="grade"><br><br>

    Section:<br>
    <input type="text" name="section"><br><br>

    <button type="submit">Add Student</button>

    </form>

    <br>
    <a href="/">Back</a>
    """

    return render_template_string(html)


# ADD STUDENT
@app.route('/add_student', methods=['POST'])
def add_student():

    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")

    new_student = {
        "id": len(students) + 1,
        "name": name,
        "grade": grade,
        "section": section
    }

    students.append(new_student)

    return redirect(url_for('list_students'))


# API GRADE CHECK
@app.route('/student')
def get_student():

    grade = int(request.args.get("grade", 0))

    return jsonify({
        "grade": grade,
        "remarks": remarks(grade)
    })


# DELETE STUDENT
@app.route('/delete/<int:id>')
def delete_student(id):

    global students
    students = [s for s in students if s["id"] != id]

    return redirect(url_for('list_students'))


# SUMMARY ANALYTICS
@app.route('/summary')
def summary():

    grades = [s["grade"] for s in students]

    passed = len([g for g in grades if g >= 75])
    failed = len(grades) - passed
    average = sum(grades) / len(grades)

    return jsonify({
        "average_grade": average,
        "passed_students": passed,
        "failed_students": failed
    })


# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)
