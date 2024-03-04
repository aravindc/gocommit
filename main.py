import requests

import os
import subprocess
import json


def get_git_diff() -> str:
    diff_output = subprocess.run(['git', 'diff'], capture_output=True, text=True)
    return diff_output.stdout.strip()

from dotenv import load_dotenv
load_dotenv()


model = os.getenv('MODEL_NAME')
url = os.getenv('ENDPOINT_URL')
stream = os.getenv('STREAM')

git_diff = get_git_diff()

json_payload = {
    "model": model,
    "prompt": "Generate and show only a concise git commit message written in present tense without return characters for the git diff: {}".format(git_diff),
    "stream": False,
}

response = requests.post(url, json=json_payload)
git_message = json.loads(response.text)['response']
print(git_message)
