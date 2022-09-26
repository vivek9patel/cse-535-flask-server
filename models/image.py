import os
from datetime import datetime

class Image:
    def __init__(self, db, storage):
        self.db = db
        self.storage = storage
        self.root = "images/"

    def create(self, image, category_id):
        try:
            image.seek(0, os.SEEK_END)
            result = None
            if image.filename != "":
                filename = "".join([c for c in image.filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()        
                path = self.root + filename
                result = self.uploadImage(image,path)
                if result and category_id:
                    self.db.child(path).push({
                        "image_url": result,
                        "category_id": category_id,
                        "created_at": datetime.now()
                    })
            
            return result
        except:
            return None
    
    def uploadImage(self, image, path):
        try:
            image.seek(0)
            self.storage.child(path).put(image)
            return self.storage.child(path).get_url()
        except:
            return None
