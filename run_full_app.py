import subprocess
import os
import platform
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(override=True)
dotenv_path = find_dotenv()
print(f"✅ Loaded .env from: {dotenv_path}")
print(f"FLASK_ENV = {os.getenv('FLASK_ENV')}")


def start_react_dev():
    """Start React development server."""
    print("⚛️ Starting React development server...")
    shell = platform.system() == "Windows"
    return subprocess.Popen(["npm", "start"], cwd="frontend", shell=shell)


def build_react():
    """Build React production files."""
    print("📦 Building React frontend...")
    subprocess.run(["npm", "run", "build"], cwd="frontend", check=True)


def run_flask():
    """Run Flask backend."""
    print("🚀 Starting Flask backend...")
    shell = platform.system() == "Windows"
    return subprocess.Popen(["python", "main.py"], cwd="backend", shell=shell)


if __name__ == "__main__":
    mode = os.getenv("FLASK_ENV", "production").lower()

    if mode == "development":
        print("🧑‍💻 Running in DEVELOPMENT mode...")
        # Start React dev server
        react_process = start_react_dev()
        # Wait a few seconds to ensure React starts
        time.sleep(5)
        # Start Flask backend
        flask_process = run_flask()

        try:
            react_process.wait()
            flask_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            react_process.terminate()
            flask_process.terminate()

    else:
        print("🚀 Running in PRODUCTION mode...")
        build_react()
        flask_process = run_flask()
        flask_process.wait()
