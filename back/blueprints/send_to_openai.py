import openai
from flask import Blueprint, send_from_directory, request, jsonify
from detector.utils import compress_jpeg
import os
import json
import base64
import requests

API_KEY = 'KAUF DIR DEIN EIGENEN API KEY' 
send_to_openai_bp = Blueprint("send_to_openai",__name__)

'''
bash command: 

sudo curl -X POST http://localhost:5000/send_to_openai
'''


@send_to_openai_bp.route('/send_to_openai', methods=['POST'])
def send_to_openai():
    try:
        # List all files in the /img folder
        img_folder = 'img'
        image_files = [f for f in os.listdir(img_folder) if f.endswith('.jpg') or f.endswith('.jpeg')]

        if not image_files:
            return jsonify({'error': 'No JPEG images found in the folder'}), 404

        image_details = {}

        for filename in image_files:
            # Construct the path to the image file
            image_path = os.path.join(img_folder, filename)

            # Read the image file and encode it as base64
            with open(image_path, 'rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            # Call the OpenAI Vision API
            openai.api_key = API_KEY
            response = send_image_to_openai(base64_image)

            # Extract description from the response
            choices = response.get('choices', [])
            if choices:
                description = choices[0]['message']['content']
            else:
                description = 'No description available'

            # Store the details for the image
            image_details[filename] = {'description': description}

        # Return the image details as JSON
        return jsonify({'image_details': image_details}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_image_to_openai(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()
