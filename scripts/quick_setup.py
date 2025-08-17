"""
Script setup cepat untuk menggunakan file baru
"""

def setup_new_files():
    """Setup dengan file yang baru diupload"""
    
    print("🚀 Jiabao Klinik - Quick Setup")
    print("=" * 40)
    
    # Input URLs
    print("📋 Masukkan URL file yang sudah diupload:")
    
    csv_url = input("🗃️  Database CSV URL: ").strip()
    
    if not csv_url:
        print("❌ URL CSV wajib diisi!")
        return
    
    # Update configuration
    from config_updater import ConfigUpdater
    updater = ConfigUpdater()
    updater.update_database_url(csv_url)
    
    # Train model dengan data baru
    print("\n🤖 Training model dengan data baru...")
    
    try:
        from face_classification_model import JiabaoFaceClassifier
        classifier = JiabaoFaceClassifier()
        accuracy = classifier.train_model(csv_url)
        
        print(f"✅ Model berhasil dilatih! Akurasi: {accuracy:.1%}")
        print("💾 Model tersimpan sebagai 'face_classifier_model.pkl'")
        
    except Exception as e:
        print(f"❌ Error training model: {e}")
        return
    
    print("\n🎉 Setup selesai!")
    print("🚀 Jalankan: streamlit run scripts/streamlit_face_app.py")

if __name__ == "__main__":
    setup_new_files()
