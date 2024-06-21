import re
from datetime import datetime
from models import Register_User, Login_User
from database import check_user, insert_user, authentication, get_password, get_username
from flask import Flask, render_template, send_file, redirect, session, request, make_response, url_for, flash
import bcrypt

app = Flask("Personal WebSite")
app.secret_key = "123"
salt = bcrypt.gensalt()

def check_valid(pattern,text):
    if re.match(pattern,text):
        return True
    else: 
        return False
    
def encrypt_hash_password(password):
    encode_password = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(encode_password, salt)
    return hashed_password

def decrypt_hash_password(password, hashed_password):
    encode_password = password.encode("utf-8")
    return bcrypt.checkpw(encode_password, hashed_password)

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        try:
            register_data = Register_User(
                first_name= request.form["first_name_register"],
                last_name= request.form["last_name_register"],
                username= request.form["username_register"],
                email= request.form["email_register"],
                age= request.form["age_register"],
                city= request.form["city_register"],
                country= request.form["country_register"],
                password= request.form["password_register"]
            )
            # current time
            join_time = datetime.now()
            join_time = join_time.strftime("%Y-%m-%d %H:%M:%S")            
            confirm_password = request.form["confirm_password_register"]

            if register_data.first_name:
                if register_data.last_name:
                    if register_data.password:
                        if register_data.password == confirm_password:
                            hashed_password = encrypt_hash_password(register_data.password)
                            if register_data.username:
                                if register_data.email:
                                    email_pattern = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$"
                                    if check_valid(email_pattern, register_data.email):
                                        if check_user(username=register_data.username, email=register_data.email):
                                            insert_user(first_name = register_data.first_name,
                                                        last_name = register_data.last_name,
                                                        username = register_data.username,
                                                        email = register_data.email,
                                                        password = hashed_password,
                                                        age = register_data.age,
                                                        country = register_data.country,
                                                        city = register_data.city,
                                                        time=join_time)
                                            flash("User Registered Successfully", "success")
                                            return render_template("login.html", flash_register="block", flash_login="none")
                                        else:
                                            flash("Username/Email Already Exists", "danger")
                                            return render_template("login.html", flash_register="block", flash_login="none")
                                    else:
                                        flash("Invalid Email", "danger")
                                        return render_template("login.html", flash_register="block", flash_login="none")
                                else:
                                    flash("Please Enter Email", "danger")
                                    return render_template("login.html", flash_register="block", flash_login="none")
                            else:
                                flash("Please Enter Username", "danger")
                                return render_template("login.html", flash_register="block", flash_login="none")
                        else:
                            flash("Password Does Not Match", "danger")
                            return render_template("login.html", flash_register="block", flash_login="none")
                    else:   
                        flash("Please Enter Password", "danger")
                        return render_template("login.html", flash_register="block", flash_login="none")
                else:
                    flash("Please Enter Your Last Name", "danger")
                    return render_template("login.html", flash_register="block", flash_login="none")
            else:
                flash("Please Enter Your First Name", "danger")
                return render_template("login.html", flash_register="block", flash_login="none")
        except:
            pass


        try:
            login_data = Login_User(
                email = request.form["email_login"],
                password = request.form["password_login"]
            )
            if login_data.email and login_data.password:
                user_password = get_password(login_data.email)
                if user_password is not None:
                    result_email_login = authentication(email=login_data.email)
                    result_password_login = decrypt_hash_password(login_data.password, user_password)
                    if result_email_login and result_password_login:
                        username = get_username(login_data.email)
                        session["username"] = username
                        return redirect(url_for("profile"))
                    else:
                        flash("Please Enter Email/Password Correctly", "danger")
                        return render_template("login.html", flash_register="none", flash_login="block")
                else:
                    flash("Please Enter Email/Password Correctly", "danger")
                    return render_template("login.html", flash_register="none", flash_login="block")
            else:
                flash("Please Enter Email/Password Correctly", "danger")
                return render_template("login.html", flash_register="none", flash_login="block")
        except:
            pass

@app.route('/download-cv')
def download_cv():
    pdf_path = 'static/pdf/AlirezaKiaeipour.pdf'
    return send_file(pdf_path, as_attachment=True)


@app.route("/profile")
def profile():
    if "username" in session:
        return render_template("profile.html")
    else:
        return redirect(url_for("login"))
    
    
@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("home"))