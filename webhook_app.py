from flask import Flask, request
from main import main as run_model

app = Flask(__name__)

@app.route('/run-model', methods=['POST'])
def trigger_model():
    run_model()
    return "Model executed!", 200
