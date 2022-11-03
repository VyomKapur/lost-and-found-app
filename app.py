from flask import Flask,  render_template, request, redirect, session
from flask_pymongo import PyMongo
from functools import wraps
from user_models import User
from item_models import Item
import pymongo

app = Flask(__name__)
app.secret_key = b'\xb6\xc4D\x95\xe5\xc6\xba\x06\xbc\x9a\x8at\xb5j\x89\x18'

client = pymongo.MongoClient("mongodb+srv://vyom:qwerty123@user.dgrxeu0.mongodb.net/?retryWrites=true&w=majority", connect=False)
db = client.lost_and_found  

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

@app.route('/error')
def error():
    return render_template('error.html', error = session['error'])

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/submit/signup', methods=['GET', 'POST'])
def signed():
    res = User(db).signup()
    if 'user' not in session:
        session['error'] = res['error']
        return redirect('/error')
    return redirect('/dashboard')

@app.route('/submit/login', methods=['GET', 'POST'])
def logged():
    res = User(db).login()
    if 'user' not in session:
        session['error'] = res['error']
        return redirect('/error')
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
    items_lost, items_found, items_lost_claimed, items_found_claimed = User(db).me()
    items_lost_claimed = list(items_lost_claimed)
    items_found_claimed = list(items_found_claimed)
    users_lost = []
    users_found = []
    claimed_lost = []
    claimed_found = []
    for item in items_lost_claimed:
        for id in item['claimed_by']:
            users_lost = db.users.find({'_id': id})
            claimed_lost.append((item,list(users_lost)))
    for item in items_found_claimed:
        for id in item['claimed_by']:
            users_found = db.users.find({'_id': id})
            claimed_found.append((item,list(users_found)))
    
    return render_template('dashboard.html', user=user, items_lost=list(items_lost), items_found=list(items_found), claimed_lost=claimed_lost, claimed_found=claimed_found)

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
    return render_template('view-lost.html', items=list(items))

@app.route('/view/lost/claim/<string:id>', methods=['GET', 'POST'])
def claim_lost(id):
    claimed_by = db.lost.find_one({"_id": id})['claimed_by']
    claimed_by.append(session['user']['_id'])
    db.lost.update_one({'_id': id}, {'$set': {'claimed_by': claimed_by}})
    return redirect('/view/lost')

@app.route('/view/found', methods=['GET', 'POST'])
def view_found():
    items = Item(db).view_found()
    return render_template('view-found.html', items=list(items))

@app.route('/view/found/claim/<string:id>', methods=['GET', 'POST'])
def claim_found(id):
    claimed_by = db.found.find_one({"_id": id})['claimed_by']
    claimed_by.append(session['user']['_id'])
    db.found.update_one({'_id': id}, {'$set': {'claimed_by': claimed_by}})
    return redirect('/view/found')

@app.route('/admin')
def admin_view():
    if session['user']['is_admin'] == "False":
        return redirect('/')
    users = db.users.find({'is_admin': 'False'})
    items_lost = db.lost.find({})
    items_found = db.found.find({})
    return render_template('admin-view.html', users=users, items_lost=items_lost, items_found=items_found)

@app.route('/admin/user/delete/<string:id>', methods=['GET', 'POST'])
def delete_user(id):
    if session['user']['is_admin'] == "False":
        return redirect('/')
    db.users.delete_one({'_id':id})
    db.found.delete_many({'created_by': id})
    db.lost.delete_many({'created_by': id})
    return redirect('/admin')

@app.route('/admin/lost/delete/<string:id>', methods=['GET', 'POST'])
def delete_lost(id):
    if session['user']['is_admin'] == "False":
        return redirect('/')
    db.lost.delete_one({'_id':id})
    return redirect('/admin')

@app.route('/admin/found/delete/<string:id>', methods=['GET', 'POST'])
def delete_found(id):
    if session['user']['is_admin'] == "False":
        return redirect('/')
    db.found.delete_one({'_id':id})
    return redirect('/admin')

if __name__ == "__main__": 
    app.run(debug=True)