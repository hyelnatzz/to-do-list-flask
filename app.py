from flask import Flask, request, url_for, redirect, flash, render_template, jsonify, session
from flask_login.utils import login_user
from forms import TaskForm, loginForm, signUpForm
from models import User, taskDB
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_required, logout_user, current_user
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hyelda@localhost/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

present_date = datetime.strftime(datetime.now(), '%A, %d %B %Y')

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

##################################### HELPER ###########################################
def finishTime(start_time, duration):                                                  #
    time_lst = start_time.split(':')                                                   #
    hr, mt = [int(i) for i in time_lst]
    new_min = mt + duration
    if new_min == 60:
            hr += 1
            mt = 0
    elif new_min > 60:
            hr += 1
            mt = new_min - 60
    else:
            mt = new_min
    return ':'.join([str(i) for i in [hr, mt]])
#########################################################################################

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=False)
                return redirect( url_for('home'))
            else:
                flash('Incorrect password')
                return render_template('login.html', form=form, today=present_date)
        else:
            flash('username does not exist')
            return render_template('login.html', form=form, today=present_date)
    return render_template('login.html', form=form, today = present_date)


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = signUpForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data.strip()
        user.name = form.full_name.data.strip()
        user.password = generate_password_hash(form.password.data.strip(), method='sha256')
        user.email = form.email.data.strip()
        db.session.add(user)
        db.session.commit()
        return redirect( url_for('success'))
    return render_template('signup.html', form=form, today = present_date)

@app.route('/success')
def success():
    return render_template('success.html') 

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    print({k:v for k,v in session.items()})
    status = ['todo','doing', 'done']
    tasks = db.session.query(taskDB).filter_by(user_id = current_user.id, current_date = datetime.strftime(datetime.now(), '%d/%m/%Y'))
    tasks = sorted(tasks, key= lambda i: i.id)
    print(tasks)
    return render_template('home.html', tasks = tasks, statuses = status, today = present_date, user=current_user)

@app.route('/new/', methods=['POST', 'GET'])
@login_required
def newTask():
    form = TaskForm()
    if form.validate_on_submit():
        task = taskDB()
        task.user_id = current_user.id
        task.title = form.title.data.strip()
        task.note = form.note.data.strip()
        task.status = 'todo'
        task.duration = form.duration.data
        task.start_time = form.start_time.data.strip()
        task.finish_time = finishTime(form.start_time.data.strip(), form.duration.data)
        db.session.add(task)
        db.session.commit()
        return redirect( url_for('home'))
    return render_template('newtask.html', form=form, today = present_date)


@app.route('/edit/<int:task_id>/', methods=['POST', 'GET'])
@login_required
def editTask(task_id):
    form = TaskForm()
    task = db.session.query(taskDB).filter_by(id=task_id).one()
    if form.validate_on_submit():
        task.title = form.title.data.strip()
        task.note = form.note.data.strip()
        task.start_time = form.start_time.data.strip()
        task.duration = form.duration.data
        task.finish_time = finishTime(task.start_time, task.duration)
        db.session.add(task)
        db.session.commit()
        return redirect( url_for('home'))
    form.note.data = task.note
    form.title.data = task.title
    form.start_time.data = task.start_time
    form.duration.data = task.duration
    return render_template('edittask.html', form=form, task=task, today = present_date)


@app.route('/remove/<int:task_id>/', methods=['POST', 'GET'])
@login_required
def removeTask(task_id):
    task = db.session.query(taskDB).filter_by(id=task_id).one()
    db.session.delete(task)
    db.session.commit()
    flash('Task Deleted Successfully')
    return redirect(url_for('home'))


@app.route('/start/<int:task_id>/', methods=['POST', 'GET'])
@login_required
def startTask(task_id):
    task = db.session.query(taskDB).filter_by(id=task_id).one()
    task.status = 'doing'
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/finish/<int:task_id>/', methods=['POST', 'GET'])
@login_required
def finishTask(task_id):
    task = db.session.query(taskDB).filter_by(id=task_id).one()
    task.status = 'done'
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/restart/<int:task_id>/', methods=['POST', 'GET'])
@login_required
def restartTask(task_id):
    task = db.session.query(taskDB).filter_by(id=task_id).one()
    task.status = 'doing'
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect( url_for('login'))

@app.route('/api/<int:task_id>/')
@login_required
def taskApi(task_id):
    task = taskDB.query.filter_by(id = task_id,user_id = current_user.id).first()
    if not task:
        return redirect( url_for('home'))
    task = {'title': task.title, 'note': task.note, 'status': task.status, 'duration': task.duration, 'start_time': task.start_time, 'finish_time': task.finish_time}
    return jsonify(task_id = task)


@app.route('/api/tasks/')
@login_required
def tasksApi():
    tasks = taskDB.query.filter_by(user_id=current_user.id).all()
    if not tasks:
        flash('You have no task entered')
        return redirect(url_for('home'))
    tasks = [{'id': task.id, 'title': task.title, 'note': task.note, 'status': task.status,
            'duration': task.duration, 'start_time': task.start_time, 'finish_time': task.finish_time} for task in tasks] 
    return jsonify(tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
