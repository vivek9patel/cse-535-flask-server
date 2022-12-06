import base64
from helpers.datetime import getCurrentTimeStamp
import cv2
import numpy as np
class Image:
    def __init__(self, firebase):
        self.storage = firebase.storage()
        self.db = firebase.database()
        self.root = "images"

    def create(self, image, category_id, category):
        try:
            if image and category_id and category:
                result = self.uploadImage(image, category)
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

    def cutIntoFourImage(self,image):
        try:
            if image:
                image = base64.b64decode(image)
                nparr = np.fromstring(image, np.uint8)
                gray = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
                h, w = gray.shape

                tr = []
                tl = []
                bl = []
                br = []
                half2 = h//2
                top = gray[:half2, :]
                bottom = gray[half2:, :]
                for i in range(top.shape[0]):
                    tl.append(top[i][:half2])
                    tr.append(top[i][half2:])
                for i in range(bottom.shape[0]):
                    bl.append(bottom[i][:half2])
                    br.append(bottom[i][half2:])
                    
                tl = np.array(tl)
                tr = np.array(tr)
                bl = np.array(bl)
                br = np.array(br)
                    
                return tl,tr,bl,br
            else:
               raise Exception("Image not provided!", image)  
        except Exception as e:
            print("Image.py (cutIntoFourImage) => ", e)
            return None, None, None, None

    def uploadImage(self, image, category):
        try:
            filename = "image"+self.db.generate_key()
            if isinstance(image,str):
                image = base64.b64decode(image)
            elif image.filename:
                filename = image.filename+self.db.generate_key()
            self.storage.child("Images").child(category).child(filename).put(image)
            return self.storage.child("Images").child(category).child(filename).get_url(None)
        except Exception as e:
            print("Image.py (uploadImage) => ", e)
            return None
