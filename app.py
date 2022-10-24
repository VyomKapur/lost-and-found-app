from flask import Flask, redirect, url_for, render_template, request, flash

app = Flask(__name__)

logged_in = False 

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    user = {}
    if request.method == "POST":
        user['username'] = request.form['username']
        logged_in = True
    return render_template('welcome.html', user=user)

if __name__ == "__main__":
    app.run(debug=True)