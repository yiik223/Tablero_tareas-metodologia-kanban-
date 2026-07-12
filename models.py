from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#estructrura usuarios DB
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('Task', backref='user', lazy=True)


#estructura tareas DB
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="todo")
    priority = db.Column(db.String(20), default="Medio")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)