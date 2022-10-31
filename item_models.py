from flask import Flask, jsonify, request, session, redirect
import uuid 
import gridfs


class Item:
    def __init__(self, db):
        self.db = db
        self.fs = gridfs.GridFS(self.db)
    
    def create_lost(self):
        item_image = request.files['image-lost']
        id = uuid.uuid4().hex
        self.fs.put(item_image, filename="lost"+str(id))
        item = { 
            "_id": id,
            "name": request.form.get('item-name'),
            "description": request.form.get('description-lost'),
            "location": request.form.get('location-lost'),
            "resolved": False,
            "image": item_image.filename,
            "created_by": session['user']['_id']
        }        
        if self.db.lost.insert_one(item):
            return True
        
        return False
    
    def view_lost(self):
        items = self.db.lost.find({'resolved':False})
        
        return items
    
    def create_found(self):
        item_image = request.files['image-found']
        id = uuid.uuid4().hex
        self.fs.put(item_image, filename="found"+str(id))
        item = { 
            "_id": id,
            "name": request.form.get('item-name'),
            "description": request.form.get('description-found'),
            "location": request.form.get('location-found'),
            "resolved": False,
            "image": item_image.filename,
            "created_by": session['user']['_id']
        }        
        if self.db.found.insert_one(item):
            return True
        return False
    
    def view_found(self):
        items = self.db.found.find({'resolved':False})
        # images = []
        # for item in items:
        #     file = self.fs.find_one({'filename': 'found'+str(item['_id'])})
        #     image = file.read()
        #     images.append(image)
        return items