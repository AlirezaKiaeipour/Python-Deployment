from fastapi import FastAPI, Form, HTTPException
import sqlite3

app = FastAPI()

@app.get("/")
def read_root():
    return "ToDo List API Application"


@app.get("/tasks")
def read_task():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ToDoList")
    results = cursor.fetchall()
    return results


@app.post("/tasks")
def add_task(id:int = Form(), title:str = Form(), description:str = Form(), time:str = Form(), status:int = Form()):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO ToDoList(id, title, description, time, status) VALUES("{id}","{title}","{description}","{time}","{status}")')
    connection.commit()
    return "Task Added"


@app.delete("/tasks/{id}")
def delete_task(id:int):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ToDoList")
    results = cursor.fetchall()
    for i in results:
        if str(id) in i[0]:
            cursor.execute(f'DELETE FROM ToDoList WHERE id="{id}"')
            connection.commit()
            return "Task Deleted"


@app.put("/tasks/{id}")
def edit_task(id:int,title:str = Form(None), description:str = Form(None), time:str = Form(None), status:int = Form(None)):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    if title and description and time and status is None:
        raise HTTPException(status_code=204, detail="Please complete the information")
    else:
        cursor.execute(f'UPDATE ToDoList SET title="{title}", description="{description}", time="{time}", status="{status}" WHERE id="{id}"')
        connection.commit()
        return "Task Edited"
    