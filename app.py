from flask import Flask,  render_template, request, redirect, session
from requests import session
from models import User
import pymongo

session = {}

app = Flask(__name__)
app.secret_key = b'\xb6\xc4D\x95\xe5\xc6\xba\x06\xbc\x9a\x8at\xb5j\x89\x18'

client = pymongo.MongoClient("mongodb+srv://vyom:qwerty123@user.dgrxeu0.mongodb.net/?retryWrites=true&w=majority")
db = client.user_login_system

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit', methods=['GET', 'POST'])
def signed():
    session['user'] = User(db).signup()
    return redirect('dashboard')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    user = {}
    if request.method == "POST":
        user = session['user']
    return render_template('dashboard.html', user=user)

if __name__ == "__main__":
    app.run(debug=True)