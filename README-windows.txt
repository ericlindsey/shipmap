==============================
Ship Map Viewer - Windows Setup
==============================

1. Install Python (if needed)
------------------------------
Visit https://www.python.org/downloads/windows/
Download Python 3.11 or later.
During install, make sure to check:
  ✅ "Add Python to PATH"

2. Install Dependencies
------------------------------
Open Command Prompt.
Navigate to the folder with this project.
Then run:

    pip install -r requirements.txt

3. Start the Map
------------------------------
Double-click:
    run_shipmap.bat

This will:
- Launch the Flask server
- Display the IP address where the server is running, for example 1.1.1.1
- Open your browser to http://<IP address>:5000/
- This should work from anywhere on the ship

To stop the server, just close the terminal window running the app.

Need help? Contact eol@unm.edu.
