from helpers.datetime import getCurrentTimeStamp

class Category:
    def __init__(self,db):
        self.root = "category"
        self.db = db.child(self.root)
    
    def create(self, category_name):
        try:
            categoryID = self.findCategoryId(category_name)
            if type(categoryID) == "<class 'str'>":
                existingCount = self.db.child(self.root).child(categoryID).child("count").get()
                self.db.child(categoryID).update({
                    "count": int(existingCount) + 1,
                    "updated_at": getCurrentTimeStamp()
                })
            elif categoryID == True:
                categoryID = self.db.generate_key()
                self.db.child(categoryID).set({
                    "name": category_name,
                    "count": 1,
                    "created_at": getCurrentTimeStamp(),
                    "updated_at": getCurrentTimeStamp()
                })
            else:
                raise Exception("Aborted!")
            return categoryID
        except Exception as e:
            print("Category.py (create) => ", e)
            return None

    def findCategoryId(self, category):
        try:
            if category:
                dbCategory = self.db.order_by_child('name').equal_to(category).get()
                return dbCategory.key()
            else:
                print("Category.py (findCategoryId) => Category is None!")
                return True
        except Exception as e:
            print("Category.py (findCategoryId) => ", e)
            return False
