from flask import Flask, jsonify, request

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to my Flask API!"

# Student API with grade parameter
@app.route('/student')
def get_student():

    # Get grade from URL parameter
    grade = int(request.args.get('grade', 0))

    # Determine pass or fail
    if grade >= 75:
        remarks = "Pass"
    else:
        remarks = "Fail"

    return jsonify({
        "name": "Rhea Asmando",
        "grade": grade,
        "section": "Zechariah",
        "remarks": remarks
    })

# Another route example
@app.route('/about')
def about():
    return jsonify({
        "project": "Flask API Deployment",
        "course": "BSIT",
        "purpose": "API Deployment Activity"
    })

if __name__ == "__main__":
    app.run()
