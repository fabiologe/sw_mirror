from __future__ import print_function
import os
from flask import Blueprint, send_from_directory, request, jsonify

send_img_bp = Blueprint("send_img", __name__)

@send_img_bp.route('/send_img', methods=['POST'])
def send_img():
    try:
        data = request.get_json()
        filename = data.get('filename')
        images_directory = 'img'
        
        # Check if the requested file is inside the specific folder
        file_path = os.path.join(images_directory, filename)
        if not os.path.isfile(file_path):
            return "File not found", 404

        # Send the file
        response = send_from_directory(images_directory, filename)

        # Delete the file after sending
        os.remove(file_path)

        return response

    except Exception as e:
        print(f"Error: {str(e)}")
        return "An error occurred", 500