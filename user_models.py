from flask import Flask, jsonify, request, session, redirect, url_for
import uuid 
from passlib.hash import pbkdf2_sha256


class User:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200
    
    def __init__(self, db):
        self.db = db
    def login(self):
        user = self.db.users.find_one({
            "name": request.form.get('username'),
            "email": request.form.get('email')
        })
        
        pass_key = request.form.get('password')
        
        if user and pbkdf2_sha256.verify(pass_key, user['password']):
            return self.start_session(user)
        
        return {"error": "Invalid username or password"}
    
    def signup(self):
        user = { 
            "_id": uuid.uuid4().hex,
            "name": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "is_admin": "False"
        }
        print(user)
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        
        if self.db.users.find_one({"email": user['email']}):
            return {"error": "Email already in use"}

        if self.db.users.find_one({"name": user['name']}):
            return {"error": "Username already in use"}
        
        if self.db.users.insert_one(user):
            return self.start_session(user)
        
        return {"error": "Error signing up"}
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    def me(self):
        items_lost = self.db.lost.find({'created_by': session['user']['_id'], 'claimed_by': []})
        items_found = self.db.found.find({'created_by': session['user']['_id'], 'claimed_by': []})
        items_lost_claimed = self.db.lost.find({'created_by': session['user']['_id'], 'claimed_by': {'$ne': []}})
        items_found_claimed = self.db.found.find({'created_by': session['user']['_id'], 'claimed_by': {'$ne': []}})
        return items_lost, items_found, items_lost_claimed, items_found_claimed
