from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    registration = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(50), nullable=False)
