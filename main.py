import requests
import os
import subprocess
import json
from logzero import logger
from dotenv import load_dotenv


def get_git_diff() -> str:
    diff_output = subprocess.run(['git', 'diff'], capture_output=True, text=True)
    return diff_output.stdout.strip()


# Load environment variables
model = os.getenv('MODEL_NAME')
url = os.getenv('ENDPOINT_URL')
stream = os.getenv('STREAM')

# Load environment variables from .env file if required
if (not model) or (not url) or (not stream):
    load_dotenv()
    model = os.getenv('MODEL_NAME')
    url = os.getenv('ENDPOINT_URL')
    stream = os.getenv('STREAM')

git_diff = get_git_diff()

if not git_diff:
    print("No git diff found. Exiting.")
    exit(0)

json_payload = {
    "model": model,
    "prompt": "Generate and show only a concise git commit message written in present tense without return characters for the git diff: {}".format(git_diff),
    "stream": False,
}

response = requests.post(url, json=json_payload)
git_message = json.loads(response.text)['response']
logger.info(git_message)
