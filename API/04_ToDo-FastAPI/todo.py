from fastapi import FastAPI, Form, HTTPException
import sqlite3

app = FastAPI()

@app.get("/")
def read_root():
    return "ToDo List API Application"


@app.get("/tasks")
def read_tasks():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ToDoList")
    results = cursor.fetchall()
    return results


@app.post("/tasks")
def add_tasks(id:str = Form(), title:str = Form(), description:str = Form(), time:str = Form(), status:str = Form()):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO ToDoList(id, title, description, time, status) VALUES("{id}","{title}","{description}","{time}","{status}")')
    connection.commit()
    return "Task Added"


@app.delete("/tasks/{title}")
def delete_tasks(title:str):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ToDoList")
    results = cursor.fetchall()
    for i in results:
        if title in i[1]:
            cursor.execute(f'DELETE FROM ToDoList WHERE title="{title}"')
            connection.commit()
            return "Task Deleted"


@app.put("/tasks/{title}")
def edit_tasks(title:str, description:str = Form(None), time:str = Form(None), status:str = Form(None)):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    if title and description and time and status is None:
        raise HTTPException(status_code=404, detail="Please complete the information")
    else:
        cursor.execute(f'UPDATE ToDoList SET description="{description}", time="{time}", status="{status}" WHERE title="{title}"')
        connection.commit()
        return "Task Edited"
    