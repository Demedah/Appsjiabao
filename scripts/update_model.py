"""
Script untuk update model dengan database baru
"""
import sys
from face_classification_model import JiabaoFaceClassifier

def update_model_with_new_data(new_csv_url):
    """Update model dengan database CSV baru"""
    print("🔄 Updating model dengan database baru...")
    
    classifier = JiabaoFaceClassifier()
    
    try:
        # Train ulang model dengan data baru
        accuracy = classifier.train_model(new_csv_url)
        print(f"✅ Model berhasil diupdate!")
        print(f"📊 Akurasi baru: {accuracy:.3f}")
        print("💾 Model tersimpan sebagai 'face_classifier_model.pkl'")
        
        return True
    except Exception as e:
        print(f"❌ Error saat update model: {e}")
        return False

if __name__ == "__main__":
    NEW_DATABASE_URL = "https://euyo7snfpiouaros.public.blob.vercel-storage.com/databaseJBC.csv"
    
    print("🚀 Jiabao Klinik - Model Update Tool")
    print("=" * 50)
    
    success = update_model_with_new_data(NEW_DATABASE_URL)
    
    if success:
        print("\n✨ Model siap digunakan dengan data terbaru!")
    else:
        print("\n💥 Gagal update model. Periksa URL dan format data.")
