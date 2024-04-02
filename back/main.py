'''import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
from detector.webcam_stream import *
from detector.img_stream import *'''
from blueprints.request_img import send_img_bp
import argparse
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
vue_path = "http://localhost:5173"

app = Flask(__name__)
CORS(app, resources={
    r"/send_img/*": {"origins": vue_path},
})

app.register_blueprint(send_img_bp)


def main():
        folder_path = "img"        
        upload =  "../api/uploads"
        save_path = "detector/img_out"
        '''detector_handler()'''
        post_img(folder_path, upload)

if __name__ == "__main__":
    main()
