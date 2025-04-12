from flask import render_template, url_for, flash, redirect, request, jsonify
from . import app, db, bcrypt
from .forms import (
    LoginForm, RegistrationForm, UpdateUserInfoForm,
    UpdateUserPassword, TaskForm, UpdateTaskForm
)
from .models import User, Task
from flask_login import login_required, current_user, login_user, logout_user
import logging

logger = logging.getLogger(__name__)


# Error Handlers
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500


# Public Pages
@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


# Auth Routes
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('all_tasks'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('all_tasks'))
        flash('Login failed. Check username or password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('all_tasks'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Task Routes
@app.route("/all_tasks")
@login_required
def all_tasks():
    tasks = current_user.tasks
    return render_template('all_tasks.html', title='All Tasks', tasks=tasks)

@app.route("/add_task", methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(content=form.task_name.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task created', 'success')
        return redirect(url_for('add_task'))
    return render_template('add_task.html', title='Add Task', form=form)

@app.route("/all_tasks/<int:task_id>/update_task", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        return render_template('errors/403.html'), 403

    form = UpdateTaskForm()
    if form.validate_on_submit():
        if form.task_name.data != task.content:
            task.content = form.task_name.data
            db.session.commit()
            flash('Task updated', 'success')
        else:
            flash('No changes made', 'warning')
        return redirect(url_for('all_tasks'))

    elif request.method == 'GET':
        form.task_name.data = task.content
    return render_template('add_task.html', title='Update Task', form=form)

@app.route("/all_tasks/<int:task_id>/delete_task")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        return render_template('errors/403.html'), 403
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted', 'info')
    return redirect(url_for('all_tasks'))


# Account Management
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserInfoForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Username updated successfully', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('account.html', title='Account Settings', form=form)

@app.route("/account/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = UpdateUserPassword()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('account'))
        else:
            flash('Incorrect current password', 'danger')
    return render_template('change_password.html', title='Change Password', form=form)


# API Routes
@app.route('/tasks', methods=['POST'])
@login_required
def create_new_task():
    title = request.form.get('title')
    description = request.form.get('description')
    csrf_token = request.form.get('csrf_token')  # CSRF handled by Flask-WTF

    logger.info(f"POST /tasks with data: {request.form}")
    if not title or not description or not csrf_token:
        logger.warning("Incomplete data for POST /tasks")
        return jsonify({'error': 'Title, description, and CSRF token are required'}), 400

    task = Task(content=title, description=description, author=current_user)
    db.session.add(task)
    db.session.commit()
    logger.info(f"Task created with ID: {task.id}")
    return jsonify({'id': task.id, 'title': task.content, 'description': task.description}), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
@login_required
def get_single_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'id': task.id, 'title': task.content, 'description': task.description}), 200
