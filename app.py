from flask import Flask, redirect, request, render_template, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

db = SQLAlchemy()

"""
App Inintializations
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'postgresql://distsys_user:QSf4pRIxWRvu7o2Y00Ttk4WGKJxjcFN3@dpg-cniu07821fec73cu8s20-a.oregon-postgres.render.com/distsys'
app.config['SQLALCHEMY_DATABASE_URI'] = 'QSf4pRIxWRvu7o2Y00Ttk4WGKJxjcFN3'
app.config['SQLALCHCHEMY_TRACK_MODIFICATIONS'] = False
db - SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    registration = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@app.route('/', strict_slashes=False)
def home():
    """
    This is the main function
    """
    return (render_template('home.html'))

@app.route('/register', strict_slashes=False, methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        registration = request.form['registration']
        password = request.form['password'] 

        ## check if email exists
        existing_email = User.query.filter_by(email).first()
        if existing_email:
            flash('email already in use', 'error')
            return (render_template('register.html'))
            
        new_user = User(email=email, phone=phone, registration=registration)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful. Please log in', 'error')
        return redirect(url_for('login'))
    return (render_template('register.html'))

@app.route('/login', strict_hashes=False, methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid login', 'error')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(port=800, debug=True)