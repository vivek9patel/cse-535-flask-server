import os
from flask import Flask, request, jsonify
from helpers.firebase import db_ref
import helpers.digit_model as digitModel

port = int(os.environ.get('PORT', 8080))
app = Flask(__name__)
digitModel.loadNetwork()

@app.route('/', methods=['GET'])
def root():
    try:
        return jsonify({"success": True, "message":"Hello World!"}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/predict_portion', methods=['POST'])
def predictPortionImage():
    try:
        data = request.get_json()
        image = data['image']
        portion = data['portion']
        process = data['currentProcess']
        predictedDigit = 0
        if portion == "top":
            predictedDigit = digitModel.predictTop(image)
        elif portion == "bottom":
            predictedDigit = digitModel.predictBottom(image)
        elif portion == "left":
            predictedDigit = digitModel.predictLeft(image)
        elif portion == "right":
            predictedDigit = digitModel.predictRight(image)
        else:
            return jsonify({"success": False, "message":"Invalid Portion!"}), 400
        db_ref['process'].setPrediction(process,portion,predictedDigit)
        return jsonify({"success": True,"message":"Success", "predictedDigit": predictedDigit}), 200
    except Exception as e:
        print(e)
        return f"An Error Occured: {e}"

@app.route('/predict_digit', methods=['POST'])
def predictDigit():
    try:
        # Retriving Data from Client
        data = request.get_json()
        image = data['image']
        # Cut and Store 4 pecies of images
        top, bottom, left, right = db_ref['image'].cutIntoFourImage(image)
        # if top!=None and bottom!=None and left!=None and right!=None:
        # Start process on backend
        currentProcess = db_ref['process'].start()
        if currentProcess:
            # Saving images in Cloud Database to send it through stream
            isPhotoUploadSuccessful = db_ref['process'].upload4Image(currentProcess,top,bottom,left,right)
            if isPhotoUploadSuccessful:
                success = db_ref['process'].setState('photosUploaded')
                if success:
                    return jsonify({"success": True, "message":"Success"}), 200
                else:
                    return jsonify({"success": False, "message":"Something Went Wrong!"}), 500
            else:
                return jsonify({"success": False, "message":"Error in Uploading 4 images!"}), 500
        else:
            return jsonify({"success": False, "message":"Please complete the previous process!"}), 500
        # else:
        #     return jsonify({"success": False, "message":"Error in cutting images!"}), 500
    except Exception as e:
        print(e)
        return f"An Error Occured: {e}"

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
