
from blueprints.request_img import send_img_bp
from blueprints.run_detector import run_detector_bp
from blueprints.send_to_openai import send_to_openai_bp
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename


vue_path = "http://localhost:5000"

app = Flask(__name__)
CORS(app, resources={
    r"/send_img/*": {"origins": vue_path},
    r"/run_detector":{"origins":vue_path},
    r"/send_to_openai": {"origins": vue_path},

})


app.register_blueprint(send_img_bp)
app.register_blueprint(run_detector_bp)
app.register_blueprint(send_to_openai_bp)


if __name__ == "__main__":
    app.run(debug = True)
