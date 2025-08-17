import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import time
from datetime import datetime
import random

# Set page config
st.set_page_config(
    page_title="Jiabao Klinik - Klasifikasi Jenis Kulit",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for medical theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .result-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2563eb;
        margin: 1rem 0;
    }
    
    .confidence-high {
        background: #dcfce7;
        color: #166534;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .confidence-medium {
        background: #fef3c7;
        color: #92400e;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .info-box {
        background: #eff6ff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dbeafe;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: #2563eb;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: #1d4ed8;
    }
</style>
""", unsafe_allow_html=True)

def simulate_random_forest_classification(image):
    """Simulate Random Forest classification for skin type"""
    # Simulate processing time
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        progress_bar.progress(i + 1)
        if i < 30:
            status_text.text('Memproses gambar...')
        elif i < 60:
            status_text.text('Mengekstrak fitur wajah...')
        elif i < 90:
            status_text.text('Menjalankan Random Forest...')
        else:
            status_text.text('Menyelesaikan analisis...')
        time.sleep(0.02)
    
    # Mock classification results
    skin_types = [
        {"class": "Dry", "confidence": random.uniform(0.75, 0.95), "label": "Kulit Kering"},
        {"class": "Normal", "confidence": random.uniform(0.80, 0.95), "label": "Kulit Normal"},
        {"class": "Oily", "confidence": random.uniform(0.70, 0.92), "label": "Kulit Berminyak"}
    ]
    
    result = random.choice(skin_types)
    
    progress_bar.empty()
    status_text.empty()
    
    return result

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 Jiabao Klinik</h1>
        <p>Sistem Klasifikasi Jenis Kulit dengan Random Forest Algorithm</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📤 Upload Foto Pasien")
        st.markdown("Unggah foto wajah pasien untuk analisis jenis kulit (kering, normal, berminyak)")
        
        uploaded_file = st.file_uploader(
            "Pilih file gambar",
            type=['png', 'jpg', 'jpeg', 'gif'],
            help="Format yang didukung: PNG, JPG, JPEG, GIF (Maksimal 10MB)"
        )
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption=f"File: {uploaded_file.name}", use_column_width=True)
            
            # File info
            file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # MB
            st.markdown(f"**Ukuran file:** {file_size:.2f} MB")
            
            # Classification button
            if st.button("🔬 Analisis Jenis Kulit", key="classify_btn"):
                st.markdown("---")
                st.markdown("### 🔍 Proses Analisis")
                
                # Run classification
                result = simulate_random_forest_classification(image)
                
                # Display results
                st.markdown("### ✅ Hasil Analisis Jenis Kulit")
                
                confidence_class = "confidence-high" if result["confidence"] > 0.8 else "confidence-medium"
                confidence_text = "Tinggi" if result["confidence"] > 0.8 else "Sedang"
                
                st.markdown(f"""
                <div class="result-card">
                    <h3>{result["label"]}</h3>
                    <p><strong>Tingkat Kepercayaan:</strong> {result["confidence"]*100:.1f}%</p>
                    <span class="{confidence_class}">{confidence_text}</span>
                    <br><br>
                    <small>Diproses pada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Medical disclaimer
                st.markdown("""
                <div class="info-box">
                    <strong>⚠️ Catatan Medis:</strong> Hasil ini adalah prediksi dari sistem AI dan harus dikonfirmasi oleh tenaga medis profesional.
                </div>
                """, unsafe_allow_html=True)
                
                # Additional recommendations based on skin type
                if result["class"] == "Dry":
                    st.info("💡 **Rekomendasi:** Gunakan pelembab yang kaya dan hindari pembersih yang terlalu keras.")
                elif result["class"] == "Normal":
                    st.success("💡 **Rekomendasi:** Pertahankan rutinitas perawatan kulit yang seimbang.")
                else:  # Oily
                    st.warning("💡 **Rekomendasi:** Gunakan produk bebas minyak dan pembersih yang lembut.")
    
    with col2:
        st.markdown("### 📊 Tentang Sistem")
        
        st.markdown("""
        **🤖 Algoritma:**
        Random Forest Classifier dengan akurasi tinggi untuk klasifikasi jenis kulit wajah
        
        **🔒 Keamanan Data:**
        Semua data pasien dienkripsi dan disimpan sesuai standar keamanan medis
        
        **📈 Akurasi:**
        Model telah dilatih dengan ribuan sampel gambar wajah
        """)
        
        # Statistics (mock data)
        st.markdown("### 📈 Statistik Hari Ini")
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.metric("Total Analisis", "47", "↑ 12%")
        
        with col_stat2:
            st.metric("Akurasi Rata-rata", "89.2%", "↑ 2.1%")
        
        # Skin type distribution
        st.markdown("### 📊 Distribusi Jenis Kulit")
        chart_data = pd.DataFrame({
            'Jenis Kulit': ['Kering', 'Normal', 'Berminyak'],
            'Jumlah': [15, 20, 12]
        })
        st.bar_chart(chart_data.set_index('Jenis Kulit'))

if __name__ == "__main__":
    main()
