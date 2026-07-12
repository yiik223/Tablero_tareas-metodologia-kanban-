from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Task

#Configuracion BD
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)




#POST es para subnir cambios y pos GET es para obtener infomracion, PUT es actualizar alguna tabla existente.
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority","Medio")

        if len(title) < 3:
            return "el titulo debe tener almenos 3 caracteres", 400
        if priority not in ["Bajo","Medio","Alto"]:
            return "prioridad invalida", 400

        new_task = Task(title=title, description=description, priority = priority)
        db.session.add(new_task)
        db.session.commit()
        
        return redirect(url_for("index"))


    #conteo de tareas que se agregan.
    tasks = Task.query.all()
    todo_count = Task.query.filter_by(status="todo").count()
    doing_count = Task.query.filter_by(status="doing").count()
    done_count = Task.query.filter_by(status="done").count()


    return render_template(
        "index.html", 
        tasks=tasks,
        todo_count=todo_count,
        doing_count=doing_count,
        done_count=done_count
    )


#eliminar una tarea en base al id de esta misma.
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


#editar la lista de las tareas en base a su id.
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form["description"]
        task.status = request.form["status"]

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit.html", task=task)

@app.route("/move/<int:task_id>/<string:new_status>", methods=["POST"])
def move_task(task_id, new_status):
    task = Task.query.get_or_404(task_id)
    task.status = new_status
    db.session.commit()
    return redirect(url_for("index"))



#constructor 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


