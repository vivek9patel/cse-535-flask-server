import os
from flask import Flask, request, jsonify
from helpers.firebase import db_ref
import helpers.digit_model as digitModel

port = int(os.environ.get('PORT', 8080))
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    try:
        return jsonify({"success": True, "message":"Hello World!"}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/predict_digit', methods=['POST'])
def predictDigit():
    try:
        # Retriving Data from Client
        data = request.get_json()
        image = data['image']
        # Predicting Digit
        predictedDigit = digitModel.predict(image)
        print("predictedDigit",predictedDigit)
        # Saving image in Cloud Database
        category_id = db_ref['category'].create(predictedDigit)
        imageURL = db_ref['image'].create(image, category_id, predictedDigit)
        # Return Image to Client
        if imageURL:
            return jsonify({"success": True, "message":"Success", "imageURL": imageURL, "predictedDigit": predictedDigit}), 200
        else:
            return jsonify({"success": False, "message":"Something Went Wrong!"}), 500
    except Exception as e:
        print(e)
        return f"An Error Occured: {e}"


if __name__ == '__main__':
    digitModel.loadNetwork()
    app.run(threaded=True, host='0.0.0.0', port=port)
