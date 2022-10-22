from flask import Flask, redirect, url_for, render_template, request, flash

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run(debug=True)