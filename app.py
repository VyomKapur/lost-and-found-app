from flask import Flask,  render_template, request, redirect, session
from flask_pymongo import PyMongo
from functools import wraps
from user_models import User
from item_models import Item
import pymongo

app = Flask(__name__)
app.secret_key = b'\xb6\xc4D\x95\xe5\xc6\xba\x06\xbc\x9a\x8at\xb5j\x89\x18'

client = pymongo.MongoClient("mongodb+srv://vyom:qwerty123@user.dgrxeu0.mongodb.net/?retryWrites=true&w=majority", connect=False)
db = client.user_login_system  

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit/signup', methods=['GET', 'POST'])
def signed():
    User(db).signup()
    return redirect('/dashboard')

@app.route('/submit/login', methods=['GET', 'POST'])
def logged():
    User(db).login()
    return redirect('/dashboard')

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
    user = session['user']
    items_lost, items_found = User(db).me()
    return render_template('dashboard.html', user=user, items_lost=items_lost, items_found=items_found)

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    return User(db).signout()

@app.route('/create/lost', methods=['GET', 'POST'])
def create_lost():
    return render_template('create-lost.html')

@app.route('/create/found', methods=['GET', 'POST'])
def create_found():
    return render_template('create-found.html')

@app.route('/submit/lost', methods=['GET', 'POST'])
def submit_lost():
    res = Item(db).create_lost()
    if res == False:
        #error  
        pass
    return redirect('/view/lost')

@app.route('/submit/found', methods=['GET', 'POST'])
def submit_found():
    Item(db).create_found()
    return redirect('/view/found')

@app.route('/view/lost', methods=['GET', 'POST'])
def view_lost():
    items = Item(db).view_lost()
    return render_template('view-lost.html', items=items)

@app.route('/view/found', methods=['GET', 'POST'])
def view_found():
    items = Item(db).view_found()
    return render_template('view-found.html', items=items)

if __name__ == "__main__": 
    app.run(debug=True)