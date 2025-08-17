"""
Script otomatis untuk setup sistem klasifikasi dengan file yang sudah diupload
"""
import subprocess
import sys
import os

def run_setup():
    """Jalankan setup otomatis dengan file user"""
    print("🚀 Jiabao Klinik - Auto Setup")
    print("=" * 50)
    
    # URLs file yang sudah diupload user
    urls = {
        'csv': 'https://euyo7snfpiouaros.public.blob.vercel-storage.com/databaseJBC.csv',
        'zip': 'https://euyo7snfpiouaros.public.blob.vercel-storage.com/Extraksi-20250817T010925Z-1-001.zip',
        'model': 'https://euyo7snfpiouaros.public.blob.vercel-storage.com/uji_coba_citra_fix%20%282%29.py'
    }
    
    print("📁 File yang akan digunakan:")
    for key, url in urls.items():
        filename = url.split('/')[-1]
        print(f"   {key.upper()}: {filename}")
    
    print("\n🔄 Memulai setup...")
    
    try:
        # 1. Update konfigurasi
        print("1️⃣ Mengupdate konfigurasi URL...")
        result = subprocess.run([sys.executable, 'scripts/config_updater.py'], 
                              input='y\n', text=True, capture_output=True)
        if result.returncode == 0:
            print("   ✅ Konfigurasi berhasil diupdate")
        else:
            print("   ⚠️ Warning pada update konfigurasi")
        
        # 2. Train model dengan data baru
        print("2️⃣ Melatih model dengan dataset baru...")
        result = subprocess.run([sys.executable, 'scripts/face_classification_model.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Model berhasil dilatih")
        else:
            print("   ⚠️ Warning pada training model")
        
        # 3. Jalankan aplikasi
        print("3️⃣ Memulai aplikasi Streamlit...")
        print("🌐 Aplikasi akan terbuka di browser...")
        print("📱 URL: http://localhost:8501")
        
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'scripts/streamlit_face_app.py'])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("🔧 Coba jalankan manual:")
        print("   1. python scripts/config_updater.py")
        print("   2. python scripts/face_classification_model.py") 
        print("   3. streamlit run scripts/streamlit_face_app.py")

if __name__ == "__main__":
    run_setup()
