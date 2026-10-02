from flask import Flask, request, redirect
import sqlite3

conn = sqlite3.connect("todo.db", check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT)")
conn.commit()

app = Flask(__name__)

tasks = ["Learn Flask", "Build portfolio"]

@app.route("/")
def index():
    rows = conn.execute("SELECT title FROM tasks").fetchall()
    html = "<h1>To-Do</h1><ul>"
    for (title,) in rows:
        html += f"<li>{title}</li>"
    html += "</ul>"
    return html

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        conn.execute("INSERT INTO tasks (title) VALUES (?)", (request.form["title"],))
        conn.commit()
        return redirect("/")
    return '<form method="post"><input name="title"><button>Add</button></form>'

if __name__ == "__main__":
    app.run(debug=True)