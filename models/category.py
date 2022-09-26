from helpers.datetime import getCurrentTimeStamp

class Category:
    def __init__(self, firebase):
        self.db = firebase.database()
        self.root = "category"
    
    def create(self, category_name):
        try:
            categoryID = self.findCategoryId(category_name)
            if categoryID == True:
                categoryID = self.db.generate_key()
                self.db.child(self.root).child(categoryID).set({
                    "name": category_name,
                    "count": 1,
                    "created_at": getCurrentTimeStamp(),
                    "updated_at": getCurrentTimeStamp()
                })
            elif categoryID == False:
               raise Exception("Aborted!")
            else:
                existingCount = self.db.child(self.root).child(categoryID).child("count").get().val()
                self.db.child(self.root).child(categoryID).update({
                    "count": int(existingCount) + 1,
                    "updated_at": getCurrentTimeStamp()
                })
            return categoryID
        except Exception as e:
            print("Category.py (create) => ", e)
            return None

    def findCategoryId(self, category):
        try:
            if category:
                response = self.db.child(self.root).order_by_child('name').equal_to(category).get()
                for category in response.each():
                    return category.key()
                return True
            else:
                print("Category.py (findCategoryId) => Category is None!")
                return False
        except Exception as e:
            print("Category.py (findCategoryId) => ", e)
            return False
