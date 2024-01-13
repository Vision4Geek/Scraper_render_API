import requests
import json
from flask import Flask, jsonify
from threading import Thread
import time

app = Flask(__name__)

# Load sites from 'sites.json'
with open('sites.json', 'r') as file:
    data = json.load(file)

SITES = data.get('sites', [])

@app.route('/')
def hello_world():
    return jsonify(message='Hello, World!')

def make_requests():
    while True:
        for site in SITES:
            response = requests.get(site)
            print(f"Site: {site}, Status Code: {response.status_code}")
        time.sleep(300)  # Send requests every 5 minutes

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = Thread(target=app.run, kwargs={'debug': True})
    flask_thread.start()

    # Start a thread to make requests to the sites
    make_requests_thread = Thread(target=make_requests)
    make_requests_thread.start()

    # Wait for both threads to finish
    flask_thread.join()
    make_requests_thread.join()
