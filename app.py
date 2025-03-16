from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import time
import threading

app = Flask(__name__)

BASE_URL = 'http://www.atlantis.whoi.edu'
TRACK_PAGE = f'{BASE_URL}/cgi-bin/imet/get_tracks'

last_fetch_time = 0
last_coords = []
lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_track_data')
def get_track_data():
    global last_fetch_time, last_coords

    with lock:
        now = time.time()
        if now - last_fetch_time < 240:
            print("Using cached track data")
            return jsonify({"track": last_coords})

        print("Fetching fresh track data...")

        res = requests.get(TRACK_PAGE)
        if not res.ok:
            return jsonify({"error": "Failed to get track page"}), 500

        soup = BeautifulSoup(res.text, 'html.parser')
        link = soup.find('a', href=lambda href: href and href.endswith('.xy'))
        if not link:
            return jsonify({"error": "No .xy link found"}), 404

        xy_url = BASE_URL + link['href']
        print(f"Fetching .xy file from: {xy_url}")
        track_res = requests.get(xy_url)
        if not track_res.ok:
            return jsonify({"error": "Failed to get .xy file"}), 500

        lines = track_res.text.strip().splitlines()
        coords = []
        for line in lines:
            try:
                x_str, y_str = line.strip().split(',')
                x = float(x_str.strip())
                y = float(y_str.strip())
                coords.append({'lat': y, 'lng': x})
            except ValueError:
                continue

        last_fetch_time = now
        last_coords = coords
        print(f"Returning {len(coords)} points")
        return jsonify({"track": coords})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
