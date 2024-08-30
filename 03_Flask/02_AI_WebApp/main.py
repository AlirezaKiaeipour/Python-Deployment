from database import get_users
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "AI API Application"

@app.get("/users")
def get_all_users():
    users = get_users()
    return users


@app.get("/users/count")
def get_all_users():
    users = get_users()
    users_list = []
    [users_list.append(user.id) for user in users]
    return len(users_list)
    