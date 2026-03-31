import subprocess
import sys
import webbrowser
import time

# Start Streamlit
process = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"]
)

# Wait for server to start
time.sleep(3)

# Open browser automatically
webbrowser.open("http://localhost:8501")

# Keep app running
process.wait()