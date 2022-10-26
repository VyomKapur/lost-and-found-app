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
            "name": request.form.get('username')
        })
        
        pass_key = request.form.get('password')
        
        if user and pbkdf2_sha256.verify(pass_key, user['password']):
            return self.start_session(user)
        
        return redirect('/')
    
    def signup(self):
        user = { 
            "_id": uuid.uuid4().hex,
            "name": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        
        if self.db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email already in use"}), 400

        if self.db.users.find_one({"name": user['name']}):
            return jsonify({"error": "Username already in use"}), 400
        
        if self.db.users.insert_one(user):
            return self.start_session(user)
        
        return jsonify({"error": "Error signing up"}), 400
    
    def signout(self):
        session.clear()
        return redirect('/')