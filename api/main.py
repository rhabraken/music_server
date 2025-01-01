from flask import Flask, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import subprocess
import shlex
from functools import wraps
import os
import re
import logging
import json

app = Flask(__name__)
CORS(app)  # Enable CORS
executor = ThreadPoolExecutor(max_workers=5)  # Allow multiple concurrent tasks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler("app.log")  # Save logs to a file
    ]
)
logger = logging.getLogger(__name__)

# Load secret token from environment variable
SECRET_TOKEN = os.getenv("API_SECRET_TOKEN")

# Middleware to log requests and responses
@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.url}")
    if request.data:
        try:
            data = json.loads(request.data)
            logger.info(f"Request Data: {json.dumps(data, indent=2)}")
        except json.JSONDecodeError:
            logger.warning("Request Data could not be parsed as JSON")

@app.after_request
def log_response_info(response):
    logger.info(f"Response: {response.status_code} {response.get_data(as_text=True)}")
    return response

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or auth != f'Bearer {SECRET_TOKEN}':
            logger.warning("Unauthorized access attempt")
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

import re

# Function to remove ANSI escape sequences
def strip_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
    return ansi_escape.sub('', text)

# Function to safely execute terminal commands
def run_command(command):
    try:
        logger.info(f"Executing command: {command}")
        # Run the command in a shell to interpret `&&`
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        # Clean up output by stripping ANSI escape codes
        clean_stdout = strip_ansi_escape_codes(result.stdout.strip())
        clean_stderr = strip_ansi_escape_codes(result.stderr.strip())
        
        output = {
            "stdout": clean_stdout,
            "stderr": clean_stderr,
            "returncode": result.returncode
        }
        
        # Log the cleaned-up result with readable formatting
        logger.info(
            f"Command Result:\n"
            f"Return Code: {output['returncode']}\n"
            f"Standard Output:\n{clean_stdout}\n"
            f"Standard Error:\n{clean_stderr}"
        )
        return output
    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        return {"error": str(e)}



# Function to handle asynchronous task
def async_download(url):
    command = f"rip -ndb url {url}" # -ndb for no duplication check
    result = run_command(command)
    
    logger.info(f"Completed async task for URL: {url}. Result:")
    logger.info(f"Return Code: {result['returncode']}")
    if result['stdout']:
        logger.info(f"Standard Output:\n{result['stdout']}")
    if result['stderr']:
        logger.info(f"Standard Error:\n{result['stderr']}")

@app.route("/", methods=["POST"])
@require_auth
def handle_request():
    data = request.json
    if not data or "url" not in data:
        logger.error("URL is required in the request")
        return jsonify({"error": "URL is required"}), 400

    url = data["url"]
    pattern = r"^https://www\.qobuz\.com/[a-zA-Z\-]+/album/[a-zA-Z0-9\-]+/[a-zA-Z0-9]+$"
    if not re.match(pattern, url):
        logger.error(f"Invalid URL format: {url}")
        return jsonify({"error": "Invalid URL format"}), 400

    logger.info(f"Received valid URL: {url}. Starting async download.")
    executor.submit(async_download, url)
    return jsonify({"message": "Download started"}), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
