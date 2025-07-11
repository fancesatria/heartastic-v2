# pip install streamlit
# pip install xgboost
# pip install joblib
# streamlit run app.py

import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("../model/xgb_heart_model.pkl")

# Label Encoder mapping
gender_map = {'Male': 1, 'Female': 0}
chestpain_map = {'typical': 0, 'atypical': 1, 'non-anginal': 2, 'asymptomatic': 3}
exercise_map = {'Yes': 1, 'No': 0}

# Title
st.title("Prediksi Risiko Penyakit Jantung")

# Input from user
age = st.number_input("Umur", min_value=20, max_value=100, value=50)
sex = st.selectbox("Jenis Kelamin", ['Male', 'Female'])
restbp = st.number_input("Tekanan Darah Istirahat", min_value=80, max_value=200, value=120)
chol = st.number_input("Kadar Kolesterol", min_value=100, max_value=400, value=200)
fbs = st.selectbox("Gula Darah Puasa > 120 mg/dl", ['Yes', 'No'])
chestpain = st.selectbox("Jenis Nyeri Dada", list(chestpain_map.keys()))
exercise = st.selectbox("Angina karena Olahraga", list(exercise_map.keys()))

# COnvert input to model's format
input_data = np.array([[
    age,
    gender_map[sex],
    chestpain_map[chestpain],
    restbp,
    chol,
    1 if fbs == 'Yes' else 0,
    exercise_map[exercise]
]])

# Button
if st.button("Prediksi"):
    prob = model.predict_proba(input_data)[0][1] 
    pred = model.predict(input_data)[0]
    st.success(f"Risiko penyakit jantung: {prob * 100:.2f}%")
    st.info("Status: " + ("Berisiko" if pred == 1 else "Tidak Berisiko"))
