# --- UPDATED ROUTES ---

@app.route('/')
def home():
    content = """
    <div class="row align-items-center py-5">
        <div class="col-lg-6">
            <h1 class="display-4 fw-bold text-dark">Student Management <span class="text-primary">Simplified.</span></h1>
            <p class="lead text-muted">A modern database system for tracking student performance and academic records efficiently.</p>
            <div class="d-grid gap-2 d-md-flex justify-content-md-start mt-4">
                <a href="/students" class="btn btn-primary btn-lg px-4 me-md-2">View Student List</a>
                <a href="/add_student_form" class="btn btn-outline-secondary btn-lg px-4">Add New Record</a>
            </div>
        </div>
        <div class="col-lg-6 d-none d-lg-block">
            <div class="card bg-primary text-white p-5 text-center">
                <i class="bi bi-database-check display-1"></i>
                <h3 class="mt-3">SQLite Powered</h3>
                <p>Permanent storage for all your student data.</p>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_HTML.replace('{% block content %}{% endblock %}', content))

@app.route('/students')
def list_students():
    all_students = Student.query.all()
    content = """
    <div class="card p-4 mb-4">
        <div class="row align-items-center mb-4">
            <div class="col-md-4">
                <h2 class="h4 m-0 fw-bold">Student Records</h2>
            </div>
            <div class="col-md-8">
                <div class="input-group">
                    <span class="input-group-text bg-white border-end-0"><i class="bi bi-search"></i></span>
                    <input type="text" id="searchInput" class="form-control border-start-0" placeholder="Search by name, section, or ID..." onkeyup="filterTable()">
                </div>
            </div>
        </div>
        <div class="table-responsive">
            <table class="table table-hover align-middle" id="studentTable">
                <thead class="table-light">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Grade</th>
                        <th>Section</th>
                        <th>Status</th>
                        <th class="text-end">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in students %}
                    <tr>
                        <td><small class="text-muted">#{{ s.id }}</small></td>
                        <td class="fw-bold">{{ s.name }}</td>
                        <td>{{ s.grade }}</td>
                        <td><span class="badge bg-light text-dark border">{{ s.section }}</span></td>
                        <td>
                            {% if s.grade >= 75 %}
                                <span class="badge badge-pass px-3">Passed</span>
                            {% else %}
                                <span class="badge badge-fail px-3">Failed</span>
                            {% endif %}
                        </td>
                        <td class="text-end">
                            <a href="/delete/{{ s.id }}" class="btn btn-sm btn-outline-danger" onclick="return confirm('Delete record?')"><i class="bi bi-trash"></i></a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    <script>
    function filterTable() {
        let input = document.getElementById("searchInput");
        let filter = input.value.toUpperCase();
        let table = document.getElementById("studentTable");
        let tr = table.getElementsByTagName("tr");
        for (let i = 1; i < tr.length; i++) {
            let rowText = tr[i].textContent || tr[i].innerText;
            if (rowText.toUpperCase().indexOf(filter) > -1) { tr[i].style.display = ""; } 
            else { tr[i].style.display = "none"; }
        }
    }
    </script>
    """
    return render_template_string(BASE_HTML.replace('{% block content %}{% endblock %}', content), students=all_students)

@app.route('/add_student_form')
def add_student_form():
    content = """
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card p-4">
                <div class="text-center mb-4">
                    <i class="bi bi-person-plus text-primary display-4"></i>
                    <h2 class="h4 mt-2">New Student Registration</h2>
                </div>
                <form action="/add_student" method="POST">
                    <div class="mb-3">
                        <label class="form-label fw-bold">Full Name</label>
                        <input type="text" name="name" class="form-control form-control-lg" placeholder="Enter complete name" required>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Final Grade</label>
                            <input type="number" name="grade" class="form-control form-control-lg" min="0" max="100" placeholder="0-100" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label fw-bold">Section</label>
                            <input type="text" name="section" class="form-control form-control-lg" placeholder="e.g. IT-3B" required>
                        </div>
                    </div>
                    <div class="d-grid mt-3">
                        <button type="submit" class="btn btn-primary btn-lg">Submit Record</button>
                        <a href="/students" class="btn btn-link text-muted mt-2">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_HTML.replace('{% block content %}{% endblock %}', content))
