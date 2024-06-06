import os
import re
from database import check_user, insert_user, authentication, get_username
from flask import Flask, render_template, request, redirect, url_for, make_response
from deepface import DeepFace

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask("Website")
app.config["UPLOAD_FOLDER"] = "./uploads"
app.config["ALLOWED_EXTENSIONS"] = {"jpg", "jpeg", "png"}

def check_valid(pattern,text):
    if re.match(pattern,text):
        return True
    else: 
        return False
    
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/")
def my_root():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", show_alert="none", show_alert_success="none", show_aler_login="none")
    
    elif request.method == "POST":
        try:
            name_register = request.form["name_register"]
            email_register = request.form["email_register"]
            username_register = request.form["username_register"]
            password_register = request.form["password_register"]

            if name_register:
                if password_register:
                    if username_register:
                        if email_register:
                            email_pattern = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$"
                            if check_valid(email_pattern, email_register):
                                if check_user(username=username_register, email=email_register):
                                    insert_user(name=name_register, username=username_register, email=email_register, password=password_register)
                                    alert = "User Registered Successfully"
                                    return render_template("login.html", show_alert="none", show_alert_success="block", show_aler_login="none")
                                else:
                                    alert = "Username/Email Already Exists"
                                    return render_template("login.html", alert=alert, show_alert="block", show_alert_success="none", show_aler_login="none")
                            else:
                                alert = "Invalid Email"
                                return render_template("login.html", alert=alert, show_alert="block", show_alert_success="none", show_aler_login="none")
                        else:
                            alert = "Please Enter Email"
                            return render_template("login.html", alert=alert, show_alert="block", show_alert_success="none", show_aler_login="none")
                    else:
                        alert = "Please Enter Username"
                        return render_template("login.html", alert=alert, show_alert="block", show_alert_success="none", show_aler_login="none")
                else:
                    alert = "Please Enter Password"
                    return render_template("login.html", alert=alert, show_alert="block", show_alert_success="none",show_aler_login="none")
            else:
                alert = "Please Enter Your Name"
                return render_template("login.html", alert=alert, show_alert="block", show_alert_success="none", show_aler_login="none")
        except:
            pass


        try:
            email_login = request.form["email_login"]
            password_login = request.form["password_login"]
            result_login = authentication(email=email_login, password=password_login)
            if result_login:
                username = get_username(email_login)
                response = make_response(redirect(url_for("profile")))
                response.set_cookie("username", username)
                return response
            else:
                return render_template("login.html", show_aler_login="block", show_alert="none", show_alert_success="none")
        except:
            pass


@app.route("/profile", methods=["GET", "POST"])
def profile():
    username = request.cookies.get("username")
    if request.method == "GET":
        response = make_response(render_template("profile.html", username=username, bmr_message="none", face_analysis_message="none", btn_face_class="active", face_analysis_class="fade show active", bmr_class=""))
        return response

    elif request.method == "POST":
        try:
            image = request.files["image"]
            if image.filename == "":
                response = make_response(render_template("profile.html", username=username, bmr_message="none", face_analysis_message="none", btn_face_class="active", face_analysis_class="fade show active", bmr_class=""))
                return response
            else:
                if image and allowed_file(image.filename):
                    save_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
                    image.save(save_path)
                    result = DeepFace.analyze(
                        img_path = save_path, 
                        actions = ['age', 'gender', 'race', 'emotion'],
                    )
                    age = result[0]["age"]

                    gender = (result[0]["gender"])
                    gender = max(zip(gender.values(), gender.keys()))[1]

                    emotion = result[0]["emotion"]
                    emotion = max(zip(emotion.values(), emotion.keys()))[1]

                    race = result[0]["race"]
                    race = max(zip(race.values(), race.keys()))[1]

                response = make_response(render_template("profile.html", username=username, gender=gender, age=age, emotion=emotion, race=race, bmr_message="none", face_analysis_message="block", btn_face_class="active", face_analysis_class="fade show active", bmr_class=""))
                return response
        except:
            pass

        try:
            gender_input_bmr = request.form["gender_input"]
            weight_input_bmr = request.form["weight_input"]
            height_input_bmr = request.form["height_input"]
            age_input_bmr = request.form["age_input"]
            if gender_input_bmr and weight_input_bmr and height_input_bmr and age_input_bmr is not None:
        
                if gender_input_bmr == "man":
                    bmr = (10 * int(weight_input_bmr)) + (6.25 * int(height_input_bmr)) - (5 * int(age_input_bmr)) + 5

                elif gender_input_bmr == "woman":
                    bmr = (10 * int(weight_input_bmr)) + (6.25 * int(height_input_bmr)) - (5 * int(age_input_bmr)) - 161

                response = make_response(render_template("profile.html", username=username, bmr=bmr, bmr_message="block", face_analysis_message="none", btn_bmr_class="active", bmr_class="fade show active", face_analysis_class=""))
                return response
                
            else:
                response = make_response(render_template("profile.html", username=username, bmr_message="none", face_analysis_message="none", btn_bmr_class="active", bmr_class="fade show active", face_analysis_class=""))
                return response
        except:
            pass


@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("home")))
    response.set_cookie("username", "", expires=0)
    return response
