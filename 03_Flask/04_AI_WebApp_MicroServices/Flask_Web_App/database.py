from sqlmodel import Session, SQLModel, create_engine, select
from models import User, Comment, Post
from utils.time import relative_time, format_datatime
from datetime import datetime

# DATABASE_URL = "postgresql://username:password@some-postgres:5432/db_postgres"
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)

def text_summarization(content):
    text = content.find(".")
    if text != -1:
        return content[:text] + " ..."
    else:
        return content

def insert_user(first_name, last_name, username, email, password, age, country, city):
    result = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, age=age, country=country, city=city)
    with Session(engine) as session:
        session.add(result)
        session.commit()

def insert_comment(content, service, user_id):
    result = Comment(content=content, services=service, user_id=user_id)
    with Session(engine) as session:
        session.add(result)
        session.commit()

def insert_blog(title, content, user_id):
    result = Post(title=title, content=content, user_id=user_id)
    with Session(engine) as session:
        session.add(result)
        session.commit()

def check_user(username, email):
    with Session(engine) as session:
        result = select(User).where(User.username == username).where(User.email == email)
        user = session.exec(result).first()
        if user is None:
            return True

def check_admin(username):
    with Session(engine) as session:
        result = select(User).where(User.username == username, User.role == "admin")
        user = session.exec(result).first()
        if user:
            return user
        else:
            return None
        
def get_users():
    with Session(engine) as session:
        result = select(User)
        users = session.exec(result).all()
        return users
        
def get_username(email):
    with Session(engine) as session:
        result = select(User).where(User.email == email)
        user = session.exec(result).first()
        return user.username
    
def get_user_id_by_username(username):
    with Session(engine) as session:
        result = select(User).where(User.username == username)
        user = session.exec(result).first()
        return user.id
    
def get_name_by_username(username):
    with Session(engine) as session:
        result = select(User).where(User.username == username)
        user = session.exec(result).first()
        return user.first_name, user.last_name
    
def get_password(email):
    with Session(engine) as session:
        result = select(User).where(User.email == email)
        user = session.exec(result).first()
        if user:
            return user.password
        
def get_comment_by_service(service):
    with Session(engine) as session:
        result = (select(Comment.content, Comment.timestamp, User.first_name, User.last_name).join(User, User.id == Comment.user_id).where(Comment.services == service))
        comments = session.exec(result).all()
        comments = [(content, relative_time(timestamp), first_name, last_name) for content, timestamp, first_name, last_name in comments]
        return comments
    
def get_blog(summarization=True):
    with Session(engine) as session:
        result = (select(Post.id, Post.title, Post.content, Post.timestamp, User.first_name, User.last_name).join(User, User.id == Post.user_id))
        blog = session.exec(result).all()
        if summarization:
            blog = [(id, title, text_summarization(content), format_datatime(timestamp), first_name, last_name) for id, title, content, timestamp, first_name, last_name in blog]
        else:
            blog = [(id, title, content, format_datatime(timestamp), first_name, last_name) for id, title, content, timestamp, first_name, last_name in blog]
        return blog
    
def get_blog_by_id(id):
    with Session(engine) as session:
        result = select(Post).where(Post.id == id)
        blog = session.exec(result).first()
        return blog.title, blog.content
    
def delete_blog(id):
    with Session(engine) as session:
        result = select(Post).where(Post.id == id)
        blog = session.exec(result).one()
        session.delete(blog)
        session.commit()
        
def update_blog(id, title, content, user_id):
    with Session(engine) as session:
        result = select(Post).where(Post.id == id)
        blog = session.exec(result).first()
        if blog:
            blog.title = title
            blog.content = content
            blog.user_id = user_id
            blog.timestamp = datetime.now()
            session.add(blog)
            session.commit()
            

def authentication(email):
    with Session(engine) as session:
        result = select(User).where(User.email == email)
        user = session.exec(result).first()
        if user:
            return True
    

def update_role(username, email):
    with Session(engine) as session:
        result = select(User).where(User.username == username, User.email == email)
        user = session.exec(result).first()
        if user:
            user.role = "admin"
            session.add(user)
            session.commit()
            return user
        else:
            return None
        