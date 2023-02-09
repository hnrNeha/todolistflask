from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
with app.app_context():
        db.create_all()


@app.route("/")
def todos():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route("/add/", methods=["POST"])
def add():
    text = request.form.get("text")
    todo = Todo(text=text)
    db.session.add(todo)
    db.session.commit()
    return render_template("index.html", todos=todos)

@app.route("/complete/<int:todo_id>/")
def complete(todo_id):
    todo = Todo.query.get(todo_id)
    todo.completed = True
    db.session.commit()
    return render_template("index.html", todos=todos)

@app.route("/delete/<int:todo_id>/")
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return render_template("index.html", todos=todos)

if __name__ == "__main__":
    app.run(debug=True)