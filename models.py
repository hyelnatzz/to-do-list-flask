from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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


