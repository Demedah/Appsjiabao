import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib
import requests
import json
import cv2
from PIL import Image
import io
import base64

class JiabaoFaceClassifier:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = None
        
    def load_data(self, csv_url):
        """Load and preprocess the training data from CSV URL"""
        print("Loading data from CSV...")
        response = requests.get(csv_url)
        
        # Save CSV content to a temporary file-like object
        csv_content = io.StringIO(response.text)
        df = pd.read_csv(csv_content)
        
        print(f"Data loaded: {len(df)} samples")
        print(f"Columns: {df.columns.tolist()}")
        
        # Parse pixel features from string to list
        df['pixel_features_parsed'] = df['pixel_features'].apply(
            lambda x: json.loads(x.replace('[', '[').replace(']', ']'))
        )
        
        # Convert pixel features to individual columns
        max_features = max(len(features) for features in df['pixel_features_parsed'])
        feature_matrix = np.zeros((len(df), max_features))
        
        for i, features in enumerate(df['pixel_features_parsed']):
            feature_matrix[i, :len(features)] = features
            
        # Create feature DataFrame
        feature_columns = [f'pixel_{i}' for i in range(max_features)]
        features_df = pd.DataFrame(feature_matrix, columns=feature_columns)
        
        # Add other numerical features
        features_df['kadar_minyak'] = pd.to_numeric(df['kadar minyak'], errors='coerce')
        features_df['kadar_air'] = pd.to_numeric(df['kadar air'], errors='coerce')
        
        # Encode pore size
        pore_size_mapping = {'kecil': 0, 'sedang': 1, 'besar': 2}
        features_df['ukuran_pori'] = df['ukuran pori'].map(pore_size_mapping)
        
        # Target variable
        target = df['Tekstur Kulit']
        
        # Map target to English for consistency
        target_mapping = {'kering': 'dry', 'normal': 'normal', 'berminyak': 'oily'}
        target = target.map(target_mapping)
        
        self.feature_columns = features_df.columns.tolist()
        
        return features_df, target
    
    def train_model(self, csv_url):
        """Train the Random Forest model"""
        # Load data
        X, y = self.load_data(csv_url)
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        print("Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save model and scaler
        joblib.dump(self.model, 'face_classifier_model.pkl')
        joblib.dump(self.scaler, 'feature_scaler.pkl')
        
        return accuracy
    
    def extract_features_from_image(self, image_data):
        """Extract features from uploaded image"""
        try:
            # Convert base64 to image if needed
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                # Remove data URL prefix
                image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
            else:
                image = Image.open(image_data)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to standard size
            image = image.resize((64, 64))
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Flatten RGB values
            pixel_features = img_array.flatten()
            
            # Simulate additional features (in real implementation, these would be calculated)
            # For demo purposes, we'll use random values within realistic ranges
            np.random.seed(42)  # For reproducible results
            kadar_minyak = np.random.uniform(0.2, 0.8)
            kadar_air = np.random.uniform(0.3, 0.7)
            ukuran_pori = np.random.randint(0, 3)  # 0=kecil, 1=sedang, 2=besar
            
            # Create feature vector matching training data format
            features = np.zeros(len(self.feature_columns))
            
            # Fill pixel features (pad or truncate as needed)
            pixel_end = min(len(pixel_features), len(self.feature_columns) - 3)
            features[:pixel_end] = pixel_features[:pixel_end]
            
            # Add other features
            features[-3] = kadar_minyak
            features[-2] = kadar_air  
            features[-1] = ukuran_pori
            
            return features.reshape(1, -1)
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def predict(self, image_data):
        """Predict skin type from image"""
        if self.model is None:
            # Try to load saved model
            try:
                self.model = joblib.load('face_classifier_model.pkl')
                self.scaler = joblib.load('feature_scaler.pkl')
            except:
                return {"error": "Model not trained yet"}
        
        # Extract features
        features = self.extract_features_from_image(image_data)
        if features is None:
            return {"error": "Could not extract features from image"}
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Get class names
        classes = self.model.classes_
        
        # Create result
        result = {
            "prediction": prediction,
            "confidence": float(max(probabilities)),
            "probabilities": {
                classes[i]: float(probabilities[i]) 
                for i in range(len(classes))
            }
        }
        
        return result

# Initialize and train the model
if __name__ == "__main__":
    classifier = JiabaoFaceClassifier()
    
    csv_url = "https://euyo7snfpiouaros.public.blob.vercel-storage.com/databaseJBC.csv"
    
    try:
        accuracy = classifier.train_model(csv_url)
        print(f"\nModel training completed with accuracy: {accuracy:.3f}")
        print("Model saved as 'face_classifier_model.pkl'")
        print("Scaler saved as 'feature_scaler.pkl'")
    except Exception as e:
        print(f"Error during training: {e}")
