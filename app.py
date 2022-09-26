import os
from flask import Flask, jsonify
from helpers.firebase import db_ref

port = int(os.environ.get('PORT', 8080))
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    try:
        return jsonify({"success": True, "message":"Hello World!"}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
