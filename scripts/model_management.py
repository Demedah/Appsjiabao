"""
Tool untuk manage model dan database
"""
import os
import joblib
import pandas as pd
from datetime import datetime
from face_classification_model import JiabaoFaceClassifier

class ModelManager:
    def __init__(self):
        self.classifier = JiabaoFaceClassifier()
    
    def backup_current_model(self):
        """Backup model yang sedang digunakan"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if os.path.exists('face_classifier_model.pkl'):
            backup_name = f'face_classifier_model_backup_{timestamp}.pkl'
            os.rename('face_classifier_model.pkl', backup_name)
            print(f"📦 Model lama dibackup sebagai: {backup_name}")
    
    def train_new_model(self, csv_url, backup_old=True):
        """Train model baru dengan database baru"""
        if backup_old:
            self.backup_current_model()
        
        print("🔄 Training model baru...")
        accuracy = self.classifier.train_model(csv_url)
        
        return accuracy
    
    def validate_csv_format(self, csv_url):
        """Validasi format CSV sebelum training"""
        try:
            import requests
            import io
            
            response = requests.get(csv_url)
            df = pd.read_csv(io.StringIO(response.text))
            
            required_columns = ['FotoCS', 'pixel_features', 'kadar minyak', 'kadar air', 'ukuran pori', 'Tekstur Kulit']
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"❌ Kolom yang hilang: {missing_columns}")
                return False
            
            print("✅ Format CSV valid!")
            print(f"📊 Jumlah data: {len(df)} samples")
            print(f"🏷️ Kelas: {df['Tekstur Kulit'].unique()}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error validasi CSV: {e}")
            return False

# Contoh penggunaan
if __name__ == "__main__":
    manager = ModelManager()
    
    # URL database baru Anda
    new_database_url = "https://euyo7snfpiouaros.public.blob.vercel-storage.com/databaseJBC.csv"
    
    print("🔍 Validasi format database...")
    if manager.validate_csv_format(new_database_url):
        print("\n🚀 Training model baru...")
        accuracy = manager.train_new_model(new_database_url)
        print(f"✅ Model baru siap! Akurasi: {accuracy:.3f}")
    else:
        print("💥 Format database tidak valid!")
