import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "scripts/requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def run_streamlit():
    """Run the Streamlit application"""
    try:
        print("🚀 Starting Jiabao Klinik Face Classification System...")
        print("📱 The app will open in your browser at http://localhost:8501")
        print("🛑 Press Ctrl+C to stop the server")
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "scripts/streamlit_app.py",
            "--server.port=8501",
            "--server.address=localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Streamlit server stopped.")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    print("🏥 Jiabao Klinik - Face Classification System")
    print("=" * 50)
    
    # Install requirements first
    if install_requirements():
        # Run the Streamlit app
        run_streamlit()
    else:
        print("❌ Failed to install requirements. Please check your Python environment.")
