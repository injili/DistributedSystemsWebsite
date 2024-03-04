from flask import Flask, redirect, request, render_template, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_mail import Mail, Message
import os

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
port = 2525
smtp_server = 'sandbox.smtp.mailtrap.io'
login = '6ce599b73b2183'
password = '24df6ac777b4bf'
sender_email = 'nyarekigospel@gmail.com'
receiver_email = 'gongoro@kabarak.ac.ke'
mail = Mail(app)


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


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a temporary token for password reset
            token = os.urandom(24).hex()
            user.token = token
            db.session.commit()

            # Send password reset email
            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset', sender='your_email@example.com', recipients=[email])
            msg.body = f'Click the following link to reset your password: {reset_link}'
            mail.send(msg)

            flash('Password reset instructions sent. Check your email.', 'info')
            return redirect(url_for('login'))
        else:
            flash('Invalid email address', 'error')

    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(token=token).first()
    if not user:
        flash('Invalid or expired token', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form['password']
        user.set_password(password)
        user.token = None
        db.session.commit()

        flash('Password reset successful. Please log in with your new password.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(port=800, debug=True)