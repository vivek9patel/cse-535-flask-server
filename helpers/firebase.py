import pyrebase
from models.category import Category
from models.image import Image
import json

configFile = open('firebaseConfig.json')
fbConfig = json.load(configFile)

firebase  = pyrebase.initialize_app(fbConfig)
db = firebase.database()
storage = firebase.storage()

db_ref = {
    "image": Image(db,storage),
    "category": Category(db)
}
