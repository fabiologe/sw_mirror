from __future__ import print_function
import os
from flask import Blueprint, send_from_directory, request, jsonify

send_img_bp = Blueprint("send_img", __name__)

@send_img_bp.route('/send_img/<path:directory>', methods=['POST'])
def send_img(directory):
    try:
        if os.path.exists(directory):
            files = os.listdir(directory)
            if files:  
                return jsonify(files=files)  
            else:
                return jsonify(error='No files found in the directory'), 404
        else:
            return jsonify(error='Directory not found'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500
