"""
Script untuk mengupdate URL database dan file di semua script
"""
import os
import re

class ConfigUpdater:
    def __init__(self):
        self.files_to_update = [
            'scripts/face_classification_model.py',
            'scripts/update_model.py', 
            'scripts/streamlit_face_app.py',
            'scripts/model_management.py'
        ]
        
        self.new_urls = {
            'csv_dataset': 'https://euyo7snfpiouaros.public.blob.vercel-storage.com/databaseJBC.csv',
            'zip_photos': 'https://euyo7snfpiouaros.public.blob.vercel-storage.com/Extraksi-20250817T010925Z-1-001.zip',
            'model_file': 'https://euyo7snfpiouaros.public.blob.vercel-storage.com/uji_coba_citra_fix%20%282%29.py'
        }
    
    def update_all_urls(self):
        """Update semua URL dengan file yang sudah diupload user"""
        print("🔄 Mengupdate semua URL dengan file baru...")
        
        # Update CSV dataset URL
        self.update_database_url(self.new_urls['csv_dataset'])
        
        # Update ZIP photos URL jika diperlukan
        self.update_zip_url(self.new_urls['zip_photos'])
        
        print("✅ Semua URL berhasil diupdate!")
        print("📁 File yang digunakan:")
        print(f"   📊 Dataset: {self.new_urls['csv_dataset']}")
        print(f"   📷 Foto ZIP: {self.new_urls['zip_photos']}")
        print(f"   🤖 Model: {self.new_urls['model_file']}")
    
    def update_zip_url(self, new_zip_url):
        """Update URL ZIP foto jika ada referensi di kode"""
        print("🔄 Mengupdate URL ZIP foto...")
        
        zip_patterns = [
            r'https://[^"\']+\.zip',
            r'# ZIP_PHOTOS_URL = .*'
        ]
        
        for file_path in self.files_to_update:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add ZIP URL reference if not exists
                if 'ZIP_PHOTOS_URL' not in content:
                    # Add at the top after imports
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith('import ') or line.startswith('from '):
                            continue
                        else:
                            lines.insert(i, f'# ZIP_PHOTOS_URL = "{new_zip_url}"')
                            break
                    content = '\n'.join(lines)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Added ZIP URL to: {file_path}")
    
    def update_database_url(self, new_csv_url):
        """Update URL database CSV di semua file"""
        print("🔄 Mengupdate URL database...")
        
        # Pattern untuk mencari URL lama
        old_patterns = [
            r'https://hebbkx1anhila5yf\.public\.blob\.vercel-storage\.com/databaseJBC-[A-Za-z0-9]+\.csv',
            r'https://your-new-database-url\.vercel-storage\.com/new-data\.csv',
            r'https://your-new-blob-url\.vercel-storage\.com/your-new-database\.csv'
        ]
        
        for file_path in self.files_to_update:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace semua pattern lama dengan URL baru
                updated = False
                for pattern in old_patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, new_csv_url, content)
                        updated = True
                
                if updated:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Updated: {file_path}")
                else:
                    print(f"⚠️ No URL found in: {file_path}")
        
        print(f"🎯 Database URL berhasil diupdate ke: {new_csv_url}")
    
    def show_current_urls(self):
        """Tampilkan URL yang sedang digunakan"""
        print("📋 URL saat ini:")
        
        url_pattern = r'https://[^"\']+\.csv'
        
        for file_path in self.files_to_update:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                urls = re.findall(url_pattern, content)
                if urls:
                    print(f"\n📁 {file_path}:")
                    for url in set(urls):  # Remove duplicates
                        print(f"   🔗 {url}")

def main():
    updater = ConfigUpdater()
    
    print("🚀 Jiabao Klinik - Configuration Updater")
    print("=" * 50)
    
    print("🎯 Menggunakan file yang sudah diupload:")
    print(f"📊 CSV Dataset: databaseJBC.csv")
    print(f"📷 ZIP Foto: Extraksi-20250817T010925Z-1-001.zip") 
    print(f"🤖 Model: uji_coba_citra_fix (2).py")
    
    confirm = input("\n✅ Update semua URL dengan file ini? (y/n): ").strip().lower()
    
    if confirm in ['y', 'yes', 'ya']:
        updater.update_all_urls()
        print("\n🎉 Konfigurasi berhasil diupdate!")
        print("🔄 Silakan restart aplikasi Streamlit")
        print("▶️ Jalankan: python scripts/streamlit_face_app.py")
    else:
        # Tampilkan URL saat ini
        updater.show_current_urls()
        
        print("\n" + "=" * 50)
        print("📝 Untuk update manual:")
        
        # Interactive update
        new_url = input("\n🔗 Masukkan URL database CSV baru (atau Enter untuk skip): ").strip()
        
        if new_url:
            if new_url.startswith('https://') and new_url.endswith('.csv'):
                updater.update_database_url(new_url)
                print("\n✅ Konfigurasi berhasil diupdate!")
                print("🔄 Silakan restart aplikasi Streamlit")
            else:
                print("❌ URL tidak valid! Harus dimulai dengan https:// dan berakhir dengan .csv")
        else:
            print("⏭️ Update dibatalkan")

if __name__ == "__main__":
    main()
