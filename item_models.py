from flask import Flask, jsonify, request, session, redirect
import uuid 
import gridfs


class Item:
    def __init__(self, db):
        self.db = db

    def create_lost(self):
        item_image = request.files['image-lost']
        fs = gridfs.GridFS(self.db)
        fs.put(item_image, filename="file")
        item = { 
            "_id": uuid.uuid4().hex,
            "name": request.form.get('item-name'),
            "description": request.form.get('description-lost'),
            "location": request.form.get('location-lost'),
            "image": item_image.filename
        }        
        if self.db.lost.insert_one(item):
            return True
        
        return False
    
    def view_lost(self):
        items = self.db.lost.find({})
        
        return items
    
    def create_found(self):
        item_image = request.files['image-found']
        fs = gridfs.GridFS(self.db)
        fs.put(item_image, filename="file")
        item = { 
            "_id": uuid.uuid4().hex,
            "name": request.form.get('item-name'),
            "description": request.form.get('description-found'),
            "location": request.form.get('location-found'),
            "image": item_image.filename
        }        
        if self.db.found.insert_one(item):
            return True
        
        return False
    
    def view_found(self):
        items = self.db.found.find({})
        
        return items