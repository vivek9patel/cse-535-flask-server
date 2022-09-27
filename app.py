import os
from flask import Flask, request, jsonify
from helpers.firebase import db_ref

port = int(os.environ.get('PORT', 8080))
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    try:
        return jsonify({"success": True, "message":"Hello World!"}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/upload_image', methods=['POST'])
def uploadImage():
    try:
        data = request.get_json()
        image = data['image']
        category = data['category']
        category_id = db_ref['category'].create(category)
        imageURL = db_ref['image'].create(image, category_id, category)
        if imageURL:
            return jsonify({"success": True, "message":"Success", "imageURL": imageURL}), 200
        else:
            return jsonify({"success": False, "message":"Something Went Wrong!"}), 500
    except Exception as e:
        print(e)
        return f"An Error Occured: {e}"


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
