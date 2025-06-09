from flask import Flask
from main import main as run_model  # make sure 'main' exists and runs your workflow

app = Flask(__name__)

@app.route('/run-model', methods=['POST'])
def trigger_model():
    run_model()
    return "✅ Model executed", 200

@app.route('/', methods=['GET'])
def index():
    return "🟢 MLB HR Model Webhook is Running"
