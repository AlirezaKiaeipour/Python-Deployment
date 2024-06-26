import os
import re
import time
from datetime import datetime
from models import Login_User, Register_User 
from database import check_user, insert_user, authentication, get_username, get_password
import dotenv
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import bcrypt
from ultralytics import YOLO
import cv2
from deepface import DeepFace

env = dotenv.load_dotenv()

app = Flask("Website")
app.secret_key = os.getenv("API_KEY")
app.config["UPLOAD_FOLDER"] = "./uploads"
app.config["ALLOWED_EXTENSIONS"] = {"jpg", "jpeg", "png"}
salt = bcrypt.gensalt()
model = YOLO("yolov8s.pt")

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
                        response = make_response(redirect(url_for("profile")))
                        response.set_cookie("username", username)
                        return response
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


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" in session:
        username = request.cookies.get("username")
        if request.method == "GET":
            response = make_response(render_template("profile.html", username=username, pose_detection_message="none", face_analysis_message="none", object_detection_message="none", btn_face_class="active", face_analysis_class="fade show active", pose_class="", object_detection_class= ""))
            return response

        elif request.method == "POST":
            try:
                image = request.files["image_face"]
                if image.filename == "":
                    response = make_response(render_template("profile.html", username=username, pose_detection_message="none", face_analysis_message="none", object_detection_message="none", btn_face_class="active", face_analysis_class="fade show active", pose_class="", object_detection_class= ""))
                    return response
                else:
                    if image and allowed_file(image.filename):
                        save_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
                        image.save(save_path)
                        result = DeepFace.analyze(
                        img_path = save_path, 
                        actions = ['age'],
                        )
                        age = result[0]["age"]
                        
                    response = make_response(render_template("profile.html", username=username, age=age, pose_detection_message="none", face_analysis_message="block", object_detection_message="none", btn_face_class="active", face_analysis_class="fade show active", pose_class="", object_detection_class= ""))
                    return response
            except:
                pass

            try:
                image = request.files["image_object_detection"]
                if image.filename == "":
                    response = make_response(render_template("profile.html", username=username, pose_detection_message="none", face_analysis_message="none", object_detection_message="none", btn_object_class="active", object_detection_class= "fade show active", face_analysis_class="", pose_class=""))
                    return response
                else:
                    if image and allowed_file(image.filename):
                        save_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
                        image.save(save_path)
                        results = model(save_path)
                        annotated_image = results[0].plot()
                        save_path_annotated_image = os.path.join("static/img/", image.filename)
                        cv2.imwrite(save_path_annotated_image, annotated_image)
                        
                    response = make_response(render_template("profile.html", username=username, save_path_annotated_image=save_path_annotated_image, pose_detection_message="none", face_analysis_message="none", object_detection_message="block", btn_object_class="active", object_detection_class= "fade show active", face_analysis_class="", pose_class=""))
                    return response
            except:
                pass

            try:
                image = request.files["image_pose_detection"]
                if image.filename == "":
                    response = make_response(render_template("profile.html", username=username, pose_detection_message="none", face_analysis_message="none", object_detection_message="none", btn_pose_class="active", pose_class="fade show active", face_analysis_class="", object_detection_class= ""))
                    return response
                    
                else:
                    if image and allowed_file(image.filename):
                        save_path = os.path.join("static/img/", image.filename)
                        image.save(save_path)
                    response = make_response(redirect(url_for("pose_detection", save_path_pose=save_path)))
                    return response
            except:
                pass

            try:
                time.sleep(1)
                mind_number = request.form["number_input"]
                if mind_number is not None:
                    return redirect(url_for("mind_reader", mind_number=mind_number))
                else:
                    response = make_response(render_template("profile.html", username=username, pose_detection_message="none", face_analysis_message="none", object_detection_message="none", btn_mind_class="active", mind_class= "fade show active", face_analysis_class="", pose_class=""))
                    return response
            except:
                pass
    else:
        return redirect(url_for("login"))
    

@app.route("/pose-detection", methods=["GET", "POST"])
def pose_detection():
    if "username" in session:
        if request.method == "GET":
            save_path_pose_image = request.args.get("save_path_pose")
            response = make_response(render_template("pose-detection.html", save_path_pose_image=save_path_pose_image))
            return response
        

@app.route("/profile/read-your-mind")
def mind_reader():
    number = request.args.get("mind_number")
    return render_template("read-your-mind.html", number=number)


@app.route("/logout")
def logout():
    session.pop("username")
    response = make_response(redirect(url_for("home")))
    response.set_cookie("username", "", expires=0)
    return response
