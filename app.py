from flask import Flask, jsonify, render_template, Response, send_from_directory
import requests
from bs4 import BeautifulSoup
import time
import threading
import os

app = Flask(__name__)

BASE_URL = 'http://www.atlantis.whoi.edu'
TRACK_PAGE = f'{BASE_URL}/cgi-bin/imet/get_tracks'

last_fetch_time = 0
last_coords = []
lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/tile_sets")
def tile_sets():
    tile_dir = os.path.join(os.getcwd(), "tiles")
    try:
        all_entries = os.listdir(tile_dir)
        tile_sets = []

        for entry in all_entries:
            full_path = os.path.join(tile_dir, entry)
            if os.path.isdir(full_path):
                # Optional: skip hidden or system folders
                if entry.startswith(".") or entry == "__pycache__":
                    continue
                tile_sets.append(entry)

        return jsonify(sorted(tile_sets))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_speed")
def get_speed():
    try:
        url = "http://www.atlantis.whoi.edu/cgi-bin/db_driven_data/status_screen/update_screen.pl"
        response = requests.get(url, timeout=15)
        html = response.text

        # Find "SOG:" and extract the number before "knots"
        import re
        #match = re.search(r"SOG:\s*</b>.*?<b>\s*([\d.]+)\s*knots", html, re.IGNORECASE | re.DOTALL)
        match = re.search(r"SOG:.*?<b>\s*([-\d.]+)\s*knots", html, re.IGNORECASE | re.DOTALL)
        if match:
            speed = float(match.group(1))
            print("got speed: ", speed)
            return jsonify({"speed": speed})
        else:
            print("got speed: error")
            return jsonify({"error": "SOG not found"}), 500

    except Exception as e:
        print(f"Error fetching or parsing SOG: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/tiles/<path:filename>')
def serve_tiles(filename):
    print("Request for:", filename)
    return send_from_directory('tiles', filename)

@app.route('/get_waypoints')
def get_waypoints():
    try:
        with open('waypoints.txt', 'r') as f:
            lines = f.readlines()
        return Response("".join(lines), headers={"Access-Control-Allow-Origin": "*"})
    except Exception as e:
        return Response(f"Error: {e}", status=500)

@app.route('/get_track_data')
def get_track_data():
    global last_fetch_time, last_coords
    try:
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
                raise ValueError("No .xy file link found in HTML")

            xy_url = BASE_URL + link['href']
            print(f"Fetching .xy file from: {xy_url}")
            track_res = requests.get(xy_url)
            if not track_res.ok:
                raise ValueError("Failed to get .xy file")

            lines = track_res.text.strip().splitlines()
            if not lines:
                raise ValueError("Downloaded track file is empty")

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

    except Exception as e:
        print(f"Primary source failed, loading default track: {e}")

        try:
            # Load fallback from local static file
            with open("default_track.xy") as f:
                latlngs = []
                for line in f:
                    parts = re.split(r'[,\s]+', line.strip())
                    if len(parts) >= 2:
                        try:
                            lon = float(parts[0])
                            lat = float(parts[1])
                            latlngs.append([lat, lon])
                        except ValueError:
                            continue
            print(f"Loaded {len(latlngs)} points from fallback")
            return jsonify({"track": latlngs})

        except Exception as fallback_error:
            print(f"Fallback failed: {fallback_error}")
            return jsonify({"track": [], "error": str(fallback_error)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

