# pip install streamlit
# pip install xgboost
# pip install joblib
# streamlit run app.py

# app.py

import streamlit as st
import joblib
import numpy as np
from PIL import Image
from pathlib import Path
from streamlit_option_menu import option_menu

# --- KONFIGURASI ---
st.set_page_config(page_title="HEARTASTIC!", page_icon="💖", layout="wide")

# --- CSS KUSTOM UNTUK STYLING ---
st.markdown("""
<style>
/* Impor font dari Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Montserrat:wght@400;700&display=swap');

/* --- Pengaturan Global --- */
.stApp {
    background: linear-gradient(135deg, #462020, #301515);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}
body, p, li, label, .st-emotion-cache-16txtl3 {
    font-family: 'Montserrat', sans-serif;
    color: #FFF9EE; 
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* --- Kustomisasi Teks & Judul --- */
h1, h2, h3, .st-emotion-cache-16idsys p {
    font-family: 'Michroma', sans-serif;
}
h1, h2 {
    color: #FF4B4B;
    text-shadow: 0 0 8px rgba(255, 75, 75, 0.5);
}
h3 {
    color: #F99BB6;
}

/* --- Navbar --- */
.nav-link-selected i {
    color: white !important;
}
.nav-link:not(.nav-link-selected):hover i {
    color: #FF4B4B !important;
}

/* --- Tombol Utama (Prediksi) --- */
.stButton > button {
    border: 2px solid #FF4B4B;
    border-radius: 20px;
    background-color: transparent;
    color: #FF4B4B;
    padding: 10px 25px;
    transition: all 0.3s ease-in-out;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #FF4B4B;
    color: white;
    box-shadow: 0 0 20px rgba(255, 75, 75, 0.6);
}

/* --- Halaman Tentang Kami --- */
div[data-testid="column"] > div[data-testid="stVerticalBlock"] {
    background-color: rgba(255, 249, 238, 0.07);
    border: 1px solid rgba(249, 155, 182, 0.2);
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    height: 100%;
}
.member-name {
    font-family: 'Michroma', sans-serif;
    font-size: 1.2rem;
    font-weight: bold;
    color: #FFF9EE;
    margin-top: 1rem;
}
.member-nim {
    font-size: 1.1rem;
    color: #F99BB6;
}

/* --- Styling Form Input --- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 10px;
    border: 1px solid rgba(249, 155, 182, 0.3);
    background-color: rgba(44, 42, 46, 0.5);
    color: #FFF9EE;
}
div[data-testid="stForm"] {
    background-color: #101010;
    padding: 20px;
    border-radius: 15px;
}

/* --- Styling Tabs di Halaman Edukasi --- */
.stTabs [role="tab"] {
    font-family: 'Michroma', sans-serif;
    font-size: 16px;
    font-weight: bold;
    color: #F99BB6;
}
.stTabs [role="tab"][aria-selected="true"] {
    color: #FF4B4B;
    border-bottom-color: #FF4B4B;
}
.stTabs [data-baseweb="tab-panel"] p,
.stTabs [data-baseweb="tab-panel"] li {
    font-size: 1.1rem;
    line-height: 1.8;
}

/* --- Border Radius untuk Gambar --- */
div[data-testid="stImage"] img {
    border-radius: 15px;
}

/* --- Animasi --- */
.fade-in {
    animation: fadeIn 1s ease-in-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* --- Media Queries untuk Tampilan Mobile (Versi Lebih Stabil) --- */
@media (max-width: 768px) {
    
    /* 1. Perbaikan Navbar Mobile */
    .nav-link span {
        display: none;
    }
    .nav-link-selected span {
        display: inline;
        margin-left: 8px;
    }
    .nav-link {
        justify-content: center;
    }

    /* 2. Perbaikan Layout Kolom agar menjadi vertikal */
    div[data-testid="column"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0 !important;
    }
}
</style>
""", unsafe_allow_html=True)


# --- NAVIGASI ATAS (TOP NAVBAR) ---
selected = option_menu(
    menu_title=None,
    options=["Beranda", "Edukasi Penyakit Jantung", "Prediksi Risiko", "Tentang Kami"],
    icons=["house-heart-fill", "book-half", "activity", "people-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "10px !important", "background-color": "#201010", "border-radius": "0px"},
        "icon": {"color": "#FFF9EE", "font-size": "20px"},
        "nav-link": {
            "font-family": "Michroma, sans-serif",
            "font-size": "16px",
            "text-align": "center",
            "margin":"0px 0px",
            "color": "#FFF9EE",
            "--hover-color": "#301515",
            "border-radius": "15px"
        },
        "nav-link-selected": {"background-color": "#F24040", "color": "white", "border-radius": "15px"},
    }
)


# --- KONTEN HALAMAN (BERDASARKAN PILIHAN MENU) ---

if selected == "Beranda":
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4]) # Memberi rasio agar logo sedikit lebih kecil dari area teks
    
    with col1:
        try:
            logo = Image.open("assets/logo_heartastic.png")
            st.image(logo, width=200) # Ukuran logo disesuaikan
        except FileNotFoundError:
            st.error("Logo tidak ditemukan.")

    with col2:
        st.title("HEARTASTIC!")
        st.markdown("<h3 style='color:#FFF9EE;'>Heart Analytics System for Trend Identification and Classification</h3>", unsafe_allow_html=True)

    st.divider()

    with st.container():
        st.header("Fitur Utama Kami")
        col1, col2, col3 = st.columns(3)

        with col1:
            try:
                st.image(Image.open("assets/icon_edukasi.jpg"))
            except FileNotFoundError:
                st.warning("Gambar 'icon_edukasi.jpg' tidak ditemukan.")
            st.subheader("Edukasi Penyakit Jantung")
            st.write("Pelajari lebih dalam tentang gejala, penyebab, dan cara pencegahan penyakit jantung.")

        with col2:
            try:
                st.image(Image.open("assets/icon_prediksi.jpg"))
            except FileNotFoundError:
                st.warning("Gambar 'icon_prediksi.jpg' tidak ditemukan.")
            st.subheader("Prediksi Risiko")
            st.write("Isi form dengan data kesehatan Anda untuk melihat estimasi risiko penyakit jantung.")

        with col3:
            try:
                st.image(Image.open("assets/icon_tentang_kami.jpg"))
            except FileNotFoundError:
                st.warning("Gambar 'icon_tentang_kami.jpg' tidak ditemukan.")
            st.subheader("Tentang Kami")
            st.write("Kenali tim di balik pengembangan aplikasi Heartastic.")
            
    st.markdown("</div>", unsafe_allow_html=True)


elif selected == "Edukasi Penyakit Jantung":

    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3]) # Kolom kiri (gambar) lebih kecil dari kolom kanan (teks)

    with col1:
        try:
            image = Image.open("assets/ilustrasi_jantung.png")
            st.image(image)
        except FileNotFoundError:
            st.warning("Gambar 'ilustrasi_jantung.png' tidak ditemukan.")

    with col2:
        st.title("Edukasi Penyakit Jantung")
        st.write("Pahami lebih dalam untuk pencegahan yang lebih baik.")
        st.divider()

        tab1, tab2, tab3 = st.tabs(["**Definisi & Penyebab**", "**Gejala Umum**", "**Pencegahan**"])

        with tab1:
            st.header("Apa Itu Penyakit Jantung?")
            st.write(
                "Penyakit jantung adalah istilah umum yang mencakup berbagai kondisi yang memengaruhi jantung. "
                "Ini termasuk penyakit pembuluh darah, seperti penyakit arteri koroner; masalah irama jantung (aritmia); "
                "dan cacat jantung bawaan, di antara lainnya."
            )
            st.subheader("Penyebab Utama:")
            st.markdown("""
            - **Aterosklerosis:** Penyempitan arteri akibat penumpukan plak.
            - **Tekanan Darah Tinggi (Hipertensi):** Membuat jantung bekerja lebih keras.
            - **Diabetes:** Gula darah tinggi dapat merusak pembuluh darah dan saraf yang mengontrol jantung.
            - **Gaya Hidup:** Merokok, diet tidak sehat, kurangnya aktivitas fisik, dan obesitas.
            """)

        with tab2:
            st.header("Kenali Gejala Umumnya")
            st.warning("Gejala bisa berbeda antara pria dan wanita. Jika Anda merasakan gejala ini, segera konsultasikan dengan dokter.", icon="⚠️")
            st.markdown("""
            - **Nyeri Dada (Angina):** Rasa tertekan, berat, atau nyeri di dada.
            - **Sesak Napas:** Terutama saat beraktivitas atau bahkan saat berbaring.
            - **Kelelahan Ekstrem:** Merasa sangat lelah tanpa alasan yang jelas.
            - **Pusing atau Pingsan:** Kehilangan kesadaran secara tiba-tiba.
            - **Detak Jantung Tidak Teratur:** Palpitasi atau detak jantung yang terasa terlalu cepat atau lambat.
            """)

        with tab3:
            st.header("Langkah-Langkah Pencegahan")
            st.success("Menerapkan gaya hidup sehat adalah kunci utama pencegahan penyakit jantung.", icon="✅")
            st.markdown("""
            1.  **Makan Makanan Sehat:** Konsumsi buah, sayur, biji-bijian, dan protein tanpa lemak. Kurangi garam, gula, dan lemak jenuh.
            2.  **Rutin Berolahraga:** Lakukan aktivitas fisik setidaknya 150 menit per minggu.
            3.  **Berhenti Merokok:** Merokok adalah salah satu faktor risiko terbesar.
            4.  **Kelola Stres:** Temukan cara sehat untuk mengelola stres, seperti meditasi atau yoga.
            5.  **Periksa Kesehatan Secara Rutin:** Lakukan pemeriksaan tekanan darah, kolesterol, dan gula darah secara berkala.
            """)
            
    st.markdown("</div>", unsafe_allow_html=True)


elif selected == "Prediksi Risiko":
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.title("Cek Prediksi Risiko Anda")
    st.write("Formulir ini dirancang untuk memberikan estimasi risiko. Hasil ini tidak menggantikan diagnosis medis profesional.")
    
    # Expander untuk keterangan form
    with st.expander("ℹ️ Klik di sini untuk melihat panduan pengisian form"):
        st.write("""
        Berikut adalah panduan untuk membantu Anda mengisi data dengan benar:
        - **Tekanan Darah Istirahat:** Normalnya di bawah 120/80 mm Hg.
        - **Kadar Kolesterol:** Kadar kolesterol total yang sehat idealnya di bawah 200 mg/dL.
        - **Gula Darah Puasa:** Normalnya di bawah 100 mg/dL. Di atas 126 mg/dL biasanya mengindikasikan diabetes.
        - **Jenis Nyeri Dada:**
            - **Typical Angina:** Nyeri dada klasik yang berhubungan dengan jantung.
            - **Atypical Angina:** Nyeri dada yang kemungkinannya lebih kecil berhubungan dengan jantung.
            - **Non-anginal Pain:** Nyeri dada yang tidak berhubungan dengan jantung.
            - **Asymptomatic:** Tidak ada gejala nyeri dada sama sekali.
        """)
    
    try:
        model = joblib.load("xgb_heart_model.pkl")
    except FileNotFoundError:
        st.error("Model 'xgb_heart_model.pkl' tidak ditemukan.")
        st.stop()

    gender_map = {'Pria': 1, 'Wanita': 0}
    chestpain_map = {'Typical Angina': 0, 'Atypical Angina': 1, 'Non-anginal Pain': 2, 'Asymptomatic': 3}
    exercise_map = {'Ya': 1, 'Tidak': 0}

    with st.container():
        with st.form("prediction_form"):
            st.header("Masukkan Data Kesehatan Anda")
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Umur", min_value=20, max_value=100, value=50)
                sex = st.selectbox("Jenis Kelamin", list(gender_map.keys()))
                chestpain = st.selectbox("Jenis Nyeri Dada", list(chestpain_map.keys()))
                fbs = st.selectbox("Gula Darah Puasa > 120 mg/dl", ['Ya', 'Tidak'])
            with col2:
                restbp = st.number_input("Tekanan Darah Istirahat (mm Hg)", min_value=80, max_value=200, value=120)
                chol = st.number_input("Kadar Kolesterol (mg/dl)", min_value=100, max_value=400, value=200)
                exercise = st.selectbox("Nyeri Dada Akibat Olahraga (Angina)?", list(exercise_map.keys()))
            submitted = st.form_submit_button("Cek Hasil Prediksi")

    if submitted:
        input_data = np.array([[
            age, gender_map[sex], chestpain_map[chestpain], restbp,
            chol, 1 if fbs == 'Ya' else 0, exercise_map[exercise]
        ]])
        prob = model.predict_proba(input_data)[0][1]
        pred = model.predict(input_data)[0]
        st.divider()
        st.subheader("Hasil Analisis Anda:")
        if pred == 1:
            st.error("**Status: Berisiko Tinggi**", icon="💔")
        else:
            st.success("**Status: Berisiko Rendah**", icon="❤️")
        st.metric(label="Tingkat Risiko Penyakit Jantung", value=f"{prob * 100:.2f} %")
        st.progress(float(prob))
        st.warning("**Penting:** Hasil ini adalah prediksi dan bukan diagnosis medis. Sangat disarankan untuk berkonsultasi dengan dokter untuk pemeriksaan lebih lanjut.")
        
    st.markdown("</div>", unsafe_allow_html=True)


elif selected == "Tentang Kami":
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.title("Tentang Tim HEARTASTIC!")
    st.write("Kami adalah sekelompok mahasiswa PPTI 21 dari BINUS University yang bersemangat dalam menerapkan teknologi Artificial Intelligence (AI) untuk membantu meningkatkan kesadaran akan kesehatan jantung.")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container():
            try:
                st.image(Image.open("assets/foto_agung.jpg"))
            except FileNotFoundError:
                st.warning("foto_agung.jpg tidak ada.")
            st.markdown("<p class='member-name'>Agung Ramadhan</p>", unsafe_allow_html=True)
            st.markdown("<p class='member-nim'>2802538435</p>", unsafe_allow_html=True)
    with col2:
        with st.container():
            try:
                st.image(Image.open("assets/foto_fance.jpg"))
            except FileNotFoundError:
                st.warning("foto_fance.jpg tidak ada.")
            st.markdown("<p class='member-name'>Fance Satria Nusantara</p>", unsafe_allow_html=True)
            st.markdown("<p class='member-nim'>2802538611</p>", unsafe_allow_html=True)
    with col3:
        with st.container():
            try:
                st.image(Image.open("assets/foto_samudra.jpg"))
            except FileNotFoundError:
                st.warning("foto_samudra.jpg tidak ada.")
            st.markdown("<p class='member-name'>Samudra Bryandhika Prakoso</p>", unsafe_allow_html=True)
            st.markdown("<p class='member-nim'>2802538750</p>", unsafe_allow_html=True)
    with col4:
        with st.container():
            try:
                st.image(Image.open("assets/foto_linda.jpg"))
            except FileNotFoundError:
                st.warning("foto_linda.jpg tidak ada.")
            st.markdown("<p class='member-name'>Yauw Linda Aprilly Suryani Harta</p>", unsafe_allow_html=True)
            st.markdown("<p class='member-nim'>2802538391</p>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)