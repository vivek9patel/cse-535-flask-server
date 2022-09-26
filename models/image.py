import base64
from helpers.datetime import getCurrentTimeStamp

class Image:
    def __init__(self, firebase):
        self.storage = firebase.storage()
        self.db = firebase.database()
        self.root = "images"

    def create(self, image, category_id):
        try:
            if image and category_id:
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
            filename = "image"+self.db.generate_key()
            if isinstance(image,str):
                image = base64.b64decode(image)
            elif image.filename:
                filename = image.filename+self.db.generate_key()
            self.storage.child("Images").child(filename).put(image)
            return self.storage.child("Images").child(filename).get_url(None)
        except Exception as e:
            print("Image.py (uploadImage) => ", e)
            return None
