import os
from helpers.datetime import getCurrentTimeStamp

class Image:
    def __init__(self, firebase):
        self.storage = firebase.storage()
        self.db = firebase.database()
        self.root = "images"

    def create(self, image, category_id):
        try:
            if image and category_id:
                image.seek(0, os.SEEK_END)
                result = None
                if image and image.filename != "":
                    # filename = "".join([c for c in image.filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                    result = self.uploadImage(image)
                    if result:
                        self.db.child(self.root).push({
                            "image_url": result,
                            "category_id": category_id,
                            "created_at": getCurrentTimeStamp()
                        })
                
                return result
            else:
                raise Exception("Image or Category_id not provided!", image, category_id) 
        except Exception as e:
            print("Image.py (create) => ", e)
            return None

    def uploadImage(self, image):
        try:
            image.seek(0)
            self.storage.child(image.filename+self.db.generate_key()).put(image)
            return self.storage.child(image.filename).get_url(None)
        except Exception as e:
            print("Image.py (uploadImage) => ", e)
            return None
