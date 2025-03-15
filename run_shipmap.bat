@echo off
echo Starting Ship Map...

REM Start Flask server in a new terminal window
start cmd /k python app.py

REM Give server a second to start up
timeout /t 2 >nul

REM Open the browser to the map page
start http://localhost:5000/

exit
