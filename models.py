from flask import Flask, jsonify, request, session
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
        
        if self.db.users.insert_one(user):
            return self.start_session(user)
        
        return jsonify({"error": "Error signing up"}), 400