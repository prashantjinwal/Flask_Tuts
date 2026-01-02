from flask import Blueprint, render_template, url_for, redirect, request, flash, session
from app import db
from app.model import Task

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/")
def veiw_tasks():
    if 'user' not in session:
        return redirect(url_for("login.html"))
    task = Task.query.all()
    return render_template("tasks.html", task = task)

@task_bp.route("/add", methods=["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for("login.html"))
    title = request.form.get(title)
    if title:
        new_task = Task(title = title, status = "Pending")
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully", 'success')

    return redirect(url_for("tasks.view_tasks"))

@task_bp.route("/toggle/<int:task_id", methods=["POST"])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == "Pending":
            task.status = "Working"
        elif task.status == "Working":
            task.status = "Done"
        else:
            task.status = "Pending"
    db.session.commit()
    return redirect(url_for("tasks.view_tasks"))

@task_bp.route("/clear", methods=["POST"])
def clear_task():
    Task.query.delete()
    db.session.commit()
    flash("All tasks are cleared!!", "info")
    return redirect(url_for("tasks.view_tasks"))