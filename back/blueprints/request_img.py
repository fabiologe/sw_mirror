from __future__ import print_function
import os
from flask import Blueprint, send_from_directory, request, jsonify

send_img_bp = Blueprint("send_img", __name__)

@send_img_bp.route('/send_img/<path:directory>', methods=['POST'])
def send_img(directory):
    data = request.get_json()
    filename = data.get('filename')
    images_directory = 'img'
    
    return send_from_directory(images_directory, filename)
