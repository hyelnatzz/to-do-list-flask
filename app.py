from flask import Flask, request, url_for, redirect, flash, render_template
from forms import TaskForm
from models import taskDB
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
"""
tasks = [{'title':'Wash clothes', 'note':'Take out and clean the dirty laundry', 'status':'todo'},
         {'title': 'Practice algorithms', 'note': 'Develop some sweet a;go to solve probs', 'status': 'doing'},
         {'title': 'Submit LHTL Assignment', 'note': 'Submit learning how to learn assignments', 'status': 'done'},
         {'title': 'Verification entry', 'note': 'Just for verification', 'status': 'done'}]"""


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hyelda@localhost/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

present_date = datetime.strftime(datetime.now(), '%A, %d %B %Y')


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



@app.route('/', methods=['GET', 'POST'])
def home():
    status = ['todo','doing', 'done']
    tasks = db.session.query(taskDB).all()
    tasks = sorted(tasks, key= lambda i: i.id)
    print(tasks)
    return render_template('home.html', tasks = tasks, statuses = status, today = present_date)

@app.route('/new/', methods=['POST', 'GET'])
def newTask():
    form = TaskForm()
    if form.validate_on_submit():
        task = taskDB()
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
def removeTask(task_id):
    task = db.session.query(taskDB).filter_by(id=task_id).one()
    db.session.delete(task)
    db.session.commit()
    flash('Task Deleted Successfully')
    return redirect(url_for('home'))


@app.route('/start/<int:task_id>/', methods=['POST', 'GET'])
def startTask(task_id):
    task = db.session.query(taskDB).filter_by(id=task_id).one()
    task.status = 'doing'
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/finish/<int:task_id>/', methods=['POST', 'GET'])
def finishTask(task_id):
    task = db.session.query(taskDB).filter_by(id=task_id).one()
    task.status = 'done'
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/restart/<int:task_id>/', methods=['POST', 'GET'])
def restartTask(task_id):
    task = db.session.query(taskDB).filter_by(id=task_id).one()
    task.status = 'doing'
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
