from flask import Flask, render_template, send_file

app = Flask("Personal WebSite")

@app.route("/")
def my_root():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/projects")
def project():
    return render_template("project.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/download-cv')
def download_cv():
    pdf_path = 'static/pdf/AlirezaKiaeipour.pdf'
    return send_file(pdf_path, as_attachment=True)
