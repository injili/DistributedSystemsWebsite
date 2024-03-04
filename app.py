from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def home():
    """
    This is the main function
    """
    return (render_template('index.html'))


if __name__ == '__main__':
    app.run(port=800, debug=True)