from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

"""
App Inintializations
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db - SQLAlchemy(app)
bcrypt = Bcrypt(app)

@app.route('/', strict_slashes=False)
def home():
    """
    This is the main function
    """
    return (render_template('index.html'))


if __name__ == '__main__':
    app.run(port=800, debug=True)