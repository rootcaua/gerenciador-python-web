from itertools import count

from flask import Flask, flash, redirect, render_template, request, url_for


app = Flask(__name__)
app.secret_key = "dev-secret-key"

tasks = []
statuses = ["A fazer", "Fazendo", "Feito"]
task_ids = count(1)


def find_task(task_id):
    return next((task for task in tasks if task["id"] == task_id), None)


@app.get("/")
def index():
    selected_status = request.args.get("status", "Todos")

    if selected_status == "Todos":
        visible_tasks = tasks
    else:
        visible_tasks = [task for task in tasks if task["status"] == selected_status]

    counters = {
        status: sum(1 for task in tasks if task["status"] == status)
        for status in statuses
    }

    return render_template(
        "index.html",
        tasks=visible_tasks,
        statuses=statuses,
        selected_status=selected_status,
        counters=counters,
        total_tasks=len(tasks),
    )


@app.post("/tasks")
def create_task():
    title = request.form.get("title", "").strip()
    responsible = request.form.get("responsible", "").strip()

    if not title or not responsible:
        flash("Informe o titulo e o responsavel da tarefa.", "error")
        return redirect(url_for("index"))

    tasks.append(
        {
            "id": next(task_ids),
            "title": title,
            "responsible": responsible,
            "status": "A fazer",
        }
    )
    flash("Tarefa criada com sucesso.", "success")
    return redirect(url_for("index"))


@app.post("/tasks/<int:task_id>/status")
def update_task_status(task_id):
    task = find_task(task_id)
    new_status = request.form.get("status", "").strip()

    if task is None:
        flash("Tarefa nao encontrada.", "error")
        return redirect(url_for("index"))

    if new_status not in statuses:
        flash("Status invalido.", "error")
        return redirect(url_for("index"))

    task["status"] = new_status
    flash("Status atualizado.", "success")
    return redirect(url_for("index", status=request.form.get("current_filter", "Todos")))


@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    task = find_task(task_id)

    if task is None:
        flash("Tarefa nao encontrada.", "error")
        return redirect(url_for("index"))

    tasks.remove(task)
    flash("Tarefa removida.", "success")
    return redirect(url_for("index", status=request.form.get("current_filter", "Todos")))


@app.post("/tasks/clear")
def clear_tasks():
    tasks.clear()
    flash("Todas as tarefas foram removidas.", "success")
    return redirect(url_for("index"))


@app.post("/statuses")
def create_status():
    name = request.form.get("name", "").strip()

    if not name:
        flash("Informe o nome do status.", "error")
        return redirect(url_for("index"))

    if name in statuses:
        flash("Esse status ja existe.", "error")
        return redirect(url_for("index"))

    statuses.append(name)
    flash("Status criado com sucesso.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
