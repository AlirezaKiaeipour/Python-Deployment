import os
import re
import time
from models import Login_User, Register_User, Submit_Comment
import database
from src.face_analysis import FaceAnalysis
from src.object_detection import YOLOv8
from utils.image import encode_image
from utils.time import relative_time
import dotenv
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import bcrypt


env = dotenv.load_dotenv()

app = Flask("Website")
app.secret_key = os.getenv("API_KEY")
app.config["UPLOAD_FOLDER"] = "./uploads"
app.config["ALLOWED_EXTENSIONS"] = {"jpg", "jpeg", "png"}
salt = bcrypt.gensalt()

face_analysis = FaceAnalysis("models/det_10g.onnx", "models/genderage.onnx")
object_detector = YOLOv8("models/yolov8n.onnx")

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

@app.route("/blog")
def blog():
    blogs = database.get_blogs()
    return render_template("blog.html", blogs=blogs)

@app.route("/blog/<int:id>")
def blog_show(id):
    blogs = database.get_blogs()
    return render_template("blog_post.html", blogs=blogs)


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
                                        if database.check_user(username=register_data.username, email=register_data.email):
                                            database.insert_user(first_name = register_data.first_name,
                                                        last_name = register_data.last_name,
                                                        username = register_data.username,
                                                        email = register_data.email,
                                                        password = hashed_password,
                                                        age = register_data.age,
                                                        country = register_data.country,
                                                        city = register_data.city)
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
                user_password = database.get_password(login_data.email)
                if user_password is not None:
                    result_email_login = database.authentication(email=login_data.email)
                    result_password_login = decrypt_hash_password(login_data.password, user_password)
                    if result_email_login and result_password_login:
                        username = database.get_username(login_data.email)
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
            face_analysis_comments = database.get_comment_by_service("face_analysis")
            object_detection_comments = database.get_comment_by_service("object_detection")
            pose_detection_comments = database.get_comment_by_service("pose_detection")
            mind_reader_comments = database.get_comment_by_service("mind_reader")

            response = make_response(render_template("profile.html", username=username, face_analysis_comments=face_analysis_comments, object_detection_comments=object_detection_comments, pose_detection_comments=pose_detection_comments, mind_reader_comments=mind_reader_comments, pose_detection_message="none", face_analysis_message="none", object_detection_message="none", btn_face_class="active", face_analysis_class="fade show active", pose_class="", object_detection_class= ""))
            return response

        elif request.method == "POST":
            try:
                image = request.files["image_face"]
                if image.filename == "":
                    response = make_response(render_template("profile.html", username=username, pose_detection_message="none", face_analysis_message="none", object_detection_message="none", btn_face_class="active", face_analysis_class="fade show active", pose_class="", object_detection_class= ""))
                    return response
                else:
                    if image and allowed_file(image.filename):
                        image = Image.open(image.stream)
                        image = np.array(image)
                        gender, age = face_analysis.detect_age_gender(image)
                        
                    response = make_response(render_template("profile.html", username=username, age=age, gender=gender, pose_detection_message="none", face_analysis_message="block", object_detection_message="none", btn_face_class="active", face_analysis_class="fade show active", pose_class="", object_detection_class= ""))
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
                        image = Image.open(image.stream)
                        image = np.array(image)
                        image, labels = object_detector(image)
                        annotated_image = encode_image(image)
                        
                    response = make_response(render_template("profile.html", username=username, annotated_image=annotated_image, pose_detection_message="none", face_analysis_message="none", object_detection_message="block", btn_object_class="active", object_detection_class= "fade show active", face_analysis_class="", pose_class=""))
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
def pose_detection_file():
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

@app.route("/login-admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "GET":
        return render_template("login_admin.html")
    elif request.method == "POST":
        login_data = Login_User(
                email = request.form["email_login_admin"],
                password = request.form["password_login_admin"]
            )
        if login_data.email and login_data.password:
            user_password = database.get_password(login_data.email)
            if user_password is not None:
                result_email_login = database.authentication(email=login_data.email)
                result_password_login = decrypt_hash_password(login_data.password, user_password)
                if result_email_login and result_password_login:
                    username = database.get_username(login_data.email)
                    role = database.check_admin(username)
                    if role:
                        session["username"] = username
                        response = make_response(redirect(url_for("admin")))
                        response.set_cookie("username", username)
                        return response
                    else:
                        flash("You Are Not Admin", "danger")
                        return render_template("login_admin.html", flash_register="none", flash_login="block")
                else:
                    flash("Please Enter Email/Password Correctly", "danger")
                    return render_template("login_admin.html", flash_register="none", flash_login="block")
            else:
                flash("Please Enter Email/Password Correctly", "danger")
                return render_template("login_admin.html", flash_register="none", flash_login="block")
        else:
            flash("Please Enter Email/Password Correctly", "danger")
            return render_template("login_admin.html", flash_register="none", flash_login="block")


@app.route("/admin")
def admin():
        try:
            username = session.get("username")
            users = database.get_users()
            for user in users:
                user.join_time = relative_time(user.join_time)
            first_name, last_name = database.get_name_by_username(username)
            return make_response(render_template("admin.html", first_name=first_name, last_name=last_name, users=users))
        except:
            return redirect(url_for("login_admin"))
        

@app.route("/add-face-user-comment", methods=["POST"])
def add_face_user_comment():
    comment_data = Submit_Comment(
        content = request.form["face_analysis_text"]
        )
    if comment_data.content:
        username = session.get("username")
        user_id = database.get_user_id_by_username(username)
        database.insert_comment(content=comment_data.content, service="face_analysis", user_id=user_id)
        return make_response(redirect(url_for("profile")))
    
    
@app.route("/add-object-user-comment", methods=["POST"])
def add_object_user_comment():
    comment_data = Submit_Comment(
        content = request.form["object_detection_text"]
        )
    if comment_data.content:
        username = session.get("username")
        user_id = database.get_user_id_by_username(username)
        database.insert_comment(content=comment_data.content, service="object_detection", user_id=user_id)
        return make_response(redirect(url_for("profile")))
    
    
@app.route("/add-pose-user-comment", methods=["POST"])
def add_pose_user_comment():
    comment_data = Submit_Comment(
        content = request.form["pose_detection_text"]
        )
    if comment_data.content:
        username = session.get("username")
        user_id = database.get_user_id_by_username(username)
        database.insert_comment(content=comment_data.content, service="pose_detection", user_id=user_id)
        return make_response(redirect(url_for("profile")))
    
    
@app.route("/add-mind-user-comment", methods=["POST"])
def add_mind_user_comment():
    comment_data = Submit_Comment(
        content = request.form["mind_reader_text"]
        )
    if comment_data.content:
        username = session.get("username")
        user_id = database.get_user_id_by_username(username)
        database.insert_comment(content=comment_data.content, service="mind_reader", user_id=user_id)
        return make_response(redirect(url_for("profile")))
    

@app.route("/admin-comment", methods=["GET", "POST"])
def admin_comment():
    username = request.cookies.get("username")
    if username:
        if request.method == "GET":
            return make_response(render_template("admin_comment.html"))
        elif request.method == "POST":
            comments_option = request.form.get("options")
            comments = database.get_comment_by_service(comments_option)
            return make_response(render_template("admin_comment.html", comments=comments))
    else:
        return redirect(url_for("login_admin"))


@app.route("/admin-setting", methods=["GET", "POST"])
def admin_setting():
    username = request.cookies.get("username")
    if username:
        if request.method == "GET":
            return make_response(render_template("admin_setting.html"))
        elif request.method == "POST":
            user = request.form["username_update_admin"]
            email = request.form["email_update_admin"]
            user = database.update_role(user, email)
            if user is not None:
                flash("User Change Admin Successfully", "success")
                return make_response(render_template("admin_setting.html", flash_update_admin="block"))
            else:
                flash("Please Enter Email/Username Correctly", "danger")
                return make_response(render_template("admin_setting.html", flash_update_admin="block"))
    else:
        return redirect(url_for("login_admin"))


@app.route("/admin-blog", methods=["GET", "POST"])
def admin_blog():
    username = request.cookies.get("username")
    if username:
        if request.method == "GET":
            blogs = database.get_blogs()
            return make_response(render_template("admin_blog.html", blogs=blogs))
        elif request.method == "POST":
            comments_option = request.form.get("options")
            comments = database.get_comment_by_service(comments_option)
            return make_response(render_template("admin_comment.html", comments=comments))
    else:
        return redirect(url_for("login_admin"))
    

@app.route("/admin-blog/new-post", methods=["GET", "POST"])
def admin_blog_new_post():
    username = request.cookies.get("username")
    if username:
        if request.method == "GET":
            return make_response(render_template("admin_blog_new_post.html"))
        elif request.method == "POST":
            title = request.form["blog_title_new_post"]
            head = request.form["blog_head_new_post"]
            content = request.form["blog_content_new_post"]
            user_id = database.get_user_id_by_username(username)
            database.insert_blog(title=title, head=head, content=content, user_id=user_id)
            return make_response(redirect(url_for("admin_blog")))
        
@app.route("/admin-blog/del-post", methods=["POST"])
def admin_blog_delete_post():
    post_id = request.form.get("post_id_delete")
    database.delete_blog(post_id)
    return redirect(url_for("admin_blog"))


@app.route("/admin-blog/edit", methods=["POST"])
def admin_blog_edit():
    post_id = request.form.get("post_id_edit")
    title, head, content = database.get_blog_by_id(post_id)
    return make_response(render_template("admin_blog_edit_post.html", post_id=post_id, title=title, head=head, content=content))

@app.route("/admin-blog/edit-post", methods=["POST"])
def admin_blog_edit_post():
    username = request.cookies.get("username")
    if username:
        user_id = database.get_user_id_by_username(username)
        post_id = request.form.get("post_id_edit")
        title = request.form["title_update_blog"]
        head = request.form["head_update_blog"]
        content = request.form["content_update_blog"]
        database.update_blog(post_id, title, head, content, user_id)
        return redirect(url_for("admin_blog"))