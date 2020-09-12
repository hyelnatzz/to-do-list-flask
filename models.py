from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hyelda@localhost/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class taskDB(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(150), nullable= False)
    note = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    current_date = db.Column(db.String(100), default=datetime.strftime(datetime.now(), '%d/%m/%Y'))
    start_time = db.Column(db.String(15), nullable=False)
    finish_time = db.Column(db.String(15), nullable=False)


    


