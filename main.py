import os
import subprocess
import sys

# GitHub repo URL (replace with your repo)
REPO_URL = "https://github.com/k10-ketan/website-surfing-agent.git"
LOCAL_REPO_PATH = "website-surfing-agent"
SCRIPT_PATH = os.path.join(LOCAL_REPO_PATH, "script.py")

def sync_repo():
    print("🔄 Syncing repository...")
    try:
        if os.path.exists(LOCAL_REPO_PATH):
            # If repo exists, pull updates
            result = subprocess.run(
                ["git", "-C", LOCAL_REPO_PATH, "pull", "origin", "main"],
                capture_output=True, text=True, check=True
            )
            print("✅ Pulled latest changes.")
        else:
            # If repo doesn't exist, clone it
            result = subprocess.run(
                ["git", "clone", REPO_URL, LOCAL_REPO_PATH],
                capture_output=True, text=True, check=True
            )
            print("✅ Cloned repository.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def install_dependencies():
    print("📦 Installing dependencies...")
    requirements_path = os.path.join(LOCAL_REPO_PATH, "requirements.txt")
    if os.path.exists(requirements_path):
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", requirements_path],
                check=True
            )
            print("✅ Dependencies installed.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
    else:
        print("ℹ️ No requirements.txt found. Skipping dependency installation.")

def run_script():
    print("🚀 Running script.py...")
    if not os.path.exists(SCRIPT_PATH):
        print(f"❌ Error: {SCRIPT_PATH} not found.")
        sys.exit(1)
    try:
        subprocess.run([sys.executable, SCRIPT_PATH], check=True)
        print("✅ Script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Sync the repo (clone or pull)
    if sync_repo():
        # Install dependencies from requirements.txt (if present)
        install_dependencies()
        # Run the script
        run_script()
    else:
        print("❌ Failed to sync repository. Exiting.")
        sys.exit(1)