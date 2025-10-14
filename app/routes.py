from flask import Blueprint, render_template, redirect, url_for, request
from app import db
from app.models import Task
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@main.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    if title:
        new_task = Task(title=title, owner=current_user)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/complete/<int:id>')
@login_required
def complete(id):
    task = Task.query.get_or_404(id)
    if task.owner != current_user:
        return redirect(url_for('main.index'))
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    if task.owner != current_user:
        return redirect(url_for('main.index'))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.index'))
