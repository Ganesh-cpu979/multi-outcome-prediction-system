import streamlit as st
from streamlit_option_menu import option_menu
import os
import pickle
from gtts import gTTS
import time

# -------------------------------------------
# 1. SETUP & HELPER FUNCTIONS
# -------------------------------------------
st.set_page_config(page_title="Health Guard AI", layout="wide", page_icon="🏥")

# --- Fail-safe Model Loader ---
def load_model(filename):
    try:
        if os.path.exists(filename):
            return pickle.load(open(filename, 'rb'))
    except:
        return None
    return None

# Load Models
diabetes_model = load_model('diabetes_model.sav')
heart_model = load_model('heart_model.sav')
kidney_model = load_model('kidney_model.sav')

# --- SPEAK FUNCTION (Aawaz Wapas Aa Gayi) 🔊 ---
def speak(text):
    try:
        # File name change kiya taaki purana audio clash na kare
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save("result_audio.mp3")
        st.audio("result_audio.mp3")
    except Exception as e:
        st.error("Audio Error (Check Internet)")

# --- SUGGESTIONS DICTIONARY (Salah Wapas Aa Gayi) 💡 ---
suggestions = {
    'dia_safe': "Great! You are healthy. Eat green vegetables, walk daily for 30 mins, and drink 3L water.",
    'dia_risk': "Alert! High Risk of Diabetes. Avoid sugar, rice, and potatoes. Consult a doctor immediately.",
    
    'hrt_safe': "Your Heart is Healthy. Keep doing cardio exercises and manage stress.",
    'hrt_risk': "Warning! Heart Issue Detected. Avoid oily food, ghee, and butter. Visit a Cardiologist.",
    
    'kid_safe': "Kidneys are functioning well. Stay hydrated and don't hold urine for long.",
    'kid_risk': "Kidney Risk Detected. Reduce salt and protein intake. Consult a Nephrologist.",
    
    'cold_safe': "You are Fit & Fine! Keep your immunity strong.",
    'cold_mild': "You have a Mild Cold. Drink Turmeric Milk (Haldi Doodh) and take steam.",
    'cold_risk': "High Infection Risk. Please isolate yourself and visit a doctor."
}

# --- LOGIC FUNCTIONS (Backup agar Model na ho) ---
def predict_diabetes_logic(gluc, bmi, age):
    if float(gluc) > 140 or (float(bmi) > 30 and float(age) > 45): return 1
    return 0

def predict_heart_logic(cp, thalach, oldpeak):
    if int(cp) > 0 or (float(thalach) > 160 and float(oldpeak) > 1.5): return 1
    return 0

def predict_kidney_logic(bp, al, hemo):
    if float(bp) > 90 or float(al) > 1 or float(hemo) < 11: return 1
    return 0

# -------------------------------------------
# 2. SIDEBAR MENU
# -------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3004/3004458.png", width=100)
    st.title("Health Guard AI")
    selected = option_menu("Main Menu",
                           ['Diabetes Prediction', 'Heart Disease', 'Kidney Health', 'Cold & Flu Check'],
                           icons=['activity', 'heart', 'droplet', 'thermometer'],
                           default_index=0)

# -------------------------------------------
# 3. MAIN PAGES
# -------------------------------------------

# === DIABETES ===
if selected == 'Diabetes Prediction':
    st.title("🩸 Diabetes Prediction")
    c1, c2, c3 = st.columns(3)
    with c1: Pregnancies = st.text_input("Pregnancies", '0')
    with c2: Glucose = st.text_input("Glucose", '120')
    with c3: BloodPressure = st.text_input("BP", '80')
    c4, c5, c6 = st.columns(3)
    with c4: SkinThickness = st.text_input("Skin Thickness", '20')
    with c5: Insulin = st.text_input("Insulin", '80')
    with c6: BMI = st.text_input("BMI", '25')
    c7, c8 = st.columns(2)
    with c7: DPF = st.text_input("Pedigree Func", '0.5')
    with c8: Age = st.text_input("Age", '30')

    if st.button("Check Result"):
        try:
            if diabetes_model:
                inputs = [float(Pregnancies), float(Glucose), float(BloodPressure), float(SkinThickness), float(Insulin), float(BMI), float(DPF), float(Age)]
                res = diabetes_model.predict([inputs])[0]
            else:
                res = predict_diabetes_logic(Glucose, BMI, Age)
            
            st.markdown("---")
            if res == 1:
                msg = f"Result: High Risk. {suggestions['dia_risk']}"
                st.error("⚠️ **High Risk of Diabetes**")
                st.warning(f"💡 **Advice:** {suggestions['dia_risk']}")
                speak(msg)
            else:
                msg = f"Result: Healthy. {suggestions['dia_safe']}"
                st.success("✅ **You are Healthy**")
                st.info(f"💡 **Advice:** {suggestions['dia_safe']}")
                speak(msg)
        except Exception as e:
            st.error(f"Error: {e}")

# === HEART ===
elif selected == 'Heart Disease':
    st.title("❤️ Heart Disease Check")
    age = st.text_input("Age", '50')
    cp = st.selectbox("Chest Pain Type", ["Typical", "Atypical", "Non-anginal", "Asymptomatic"])
    thalach = st.text_input("Max Heart Rate", '150')
    oldpeak = st.text_input("ST Depression", '1.0')

    if st.button("Check Heart Health"):
        try:
            cp_val = 0
            if cp == "Atypical": cp_val = 1
            elif cp == "Non-anginal": cp_val = 2
            elif cp == "Asymptomatic": cp_val = 3

            if heart_model:
                inputs = [float(age), 1, cp_val, 120, 200, 0, 1, float(thalach), 0, float(oldpeak), 1, 0, 2]
                res = heart_model.predict([inputs])[0]
            else:
                res = predict_heart_logic(cp_val, thalach, oldpeak)
            
            st.markdown("---")
            if res == 1:
                msg = f"Result: Risk Detected. {suggestions['hrt_risk']}"
                st.error("⚠️ **Heart Issue Risk**")
                st.warning(f"💡 **Advice:** {suggestions['hrt_risk']}")
                speak(msg)
            else:
                msg = f"Result: Healthy. {suggestions['hrt_safe']}"
                st.success("✅ **Heart is Healthy**")
                st.info(f"💡 **Advice:** {suggestions['hrt_safe']}")
                speak(msg)
        except Exception as e:
            st.error(f"Error: {e}")

# === KIDNEY ===
elif selected == 'Kidney Health':
    st.title("🩺 Kidney Check")
    bp = st.text_input("BP", '80')
    al = st.selectbox("Albumin", [0,1,2,3,4,5])
    hemo = st.text_input("Hemoglobin", '15')

    if st.button("Check Kidney"):
        try:
            if kidney_model:
                inputs = [40, float(bp), 1.020, int(al), 0, 1, 1, 0, 0, 100, 30, 1.2, 135, 4.5, float(hemo), 40, 8000, 4.5, 0, 0, 0, 1, 0, 0]
                res = kidney_model.predict([inputs])[0]
            else:
                res = predict_kidney_logic(bp, al, hemo)
            
            st.markdown("---")
            if res == 1:
                msg = f"Result: Risk Detected. {suggestions['kid_risk']}"
                st.error("⚠️ **Kidney Issue Risk**")
                st.warning(f"💡 **Advice:** {suggestions['kid_risk']}")
                speak(msg)
            else:
                msg = f"Result: Healthy. {suggestions['kid_safe']}"
                st.success("✅ **Kidneys are Healthy**")
                st.info(f"💡 **Advice:** {suggestions['kid_safe']}")
                speak(msg)
        except Exception as e:
            st.error(f"Error: {e}")

# === COLD & FEVER (PURANA WALA LOGIC WAPAS) 🤧 ===
elif selected == 'Cold & Flu Check':
    st.title("🤧 Viral & Cold Check")
    
    col1, col2 = st.columns(2)
    with col1:
        fever = st.selectbox("Fever?", ("No", "Mild", "High"))
        cough = st.selectbox("Cough?", ("No", "Dry", "Wet"))
    with col2:
        runny = st.radio("Runny Nose?", ("No", "Yes"), horizontal=True)
        body = st.radio("Body Pain?", ("No", "Yes"), horizontal=True)
        breath = st.radio("Breathing Issue?", ("No", "Yes"), horizontal=True)
    
    if st.button("Check Viral Risk"):
        # SCORING SYSTEM (Old Logic)
        score = 0
        if fever == "High": score+=3
        elif fever == "Mild": score+=1
        if cough != "No": score+=1
        if body == "Yes": score+=2
        if breath == "Yes": score+=5
        
        st.markdown("---")
        msg = ""
        if score == 0:
            msg = f"You are Safe. {suggestions['cold_safe']}"
            st.balloons()
            st.success("✅ **You are Healthy!**")
            st.info(f"💡 **Advice:** {suggestions['cold_safe']}")
        elif score <= 4:
            msg = f"Mild Viral. {suggestions['cold_mild']}"
            st.warning("🤧 **Viral Fever / Cold**")
            st.info(f"💡 **Advice:** {suggestions['cold_mild']}")
        else:
            msg = f"High Risk. {suggestions['cold_risk']}"
            st.error("⚠️ **High Infection Risk / Flu**")
            st.warning(f"💡 **Advice:** {suggestions['cold_risk']}")
            
        speak(msg)
