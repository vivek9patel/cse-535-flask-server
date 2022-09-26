from datetime import datetime

class Category:
    def __init__(self,db):
        self.root = "category/"
        self.db = db.child(self.root)
    
    def create(self, category_name):
        try:
            existingCategoryID = self.findCategoryId(category_name)
            if existingCategoryID:
                existingCount = self.db.child(self.root).child(existingCategoryID).child("count").get()
                self.db.child(existingCategoryID).update({
                    "count": int(existingCount) + 1,
                    "updated_at": datetime.now()
                })
            else:
                self.db.push({
                    "name": category_name,
                    "count": 1,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                })
            return True
        except:
            return False

    def findCategoryId(self, category):
        try:
            dbCategory = self.db.order_by_child("name").equal_to(category).get()
            return dbCategory.key()
        except:
            return None
