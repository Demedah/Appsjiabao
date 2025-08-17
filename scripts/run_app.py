import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def run_streamlit():
    """Run the Streamlit application"""
    print("Starting Jiabao Klinik Face Classification System...")
    print("🏥 Sistem Klasifikasi Jenis Kulit - Jiabao Klinik")
    print("📊 Menggunakan Random Forest Algorithm")
    print("🌐 Aplikasi akan terbuka di browser...")
    
    # Run streamlit app
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "streamlit_face_app.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ])

if __name__ == "__main__":
    try:
        # Install requirements first
        install_requirements()
        
        # Run the app
        run_streamlit()
        
    except KeyboardInterrupt:
        print("\n👋 Aplikasi dihentikan oleh user")
    except Exception as e:
        print(f"❌ Error: {e}")
