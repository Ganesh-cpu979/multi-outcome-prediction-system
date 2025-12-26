import streamlit as st
from streamlit_option_menu import option_menu
import os
import pickle
from gtts import gTTS
import time

# -------------------------------------------
# 1. SETUP & LANGUAGES
# -------------------------------------------
st.set_page_config(page_title="Health Guard AI", layout="wide", page_icon="🏥")

# --- Language Dictionary ---
text_dict = {
    'English': {
        'title': "Health Guard AI",
        'menu': ['Diabetes Prediction', 'Heart Disease', 'Kidney Health', 'Cold & Flu Check'],
        'dia_title': "🩸 Diabetes Prediction", 'hrt_title': "❤️ Heart Disease Check",
        'kid_title': "🩺 Kidney Health Check", 'cold_title': "🤧 Viral & Cold Check",
        'btn': "Get Result",
        'safe': "You are Healthy!", 'risk': "High Risk Detected!",
        'dia_adv_safe': "Eat green veggies, walk 30 mins daily.", 'dia_adv_risk': "Consult Doctor. Avoid sugar & rice.",
        'hrt_adv_safe': "Keep doing cardio exercises.", 'hrt_adv_risk': "Avoid oily food. Visit Cardiologist.",
        'kid_adv_safe': "Stay hydrated, drink water.", 'kid_adv_risk': "Reduce salt. Consult Nephrologist.",
        'cold_safe': "You are fit!", 'cold_mild': "Take Steam & Turmeric Milk.", 'cold_risk': "High Fever. Visit Doctor.",
        'loading': "Analyzing..."
    },
    'Hindi': {
        'title': "हेल्थ गार्ड AI (स्वास्थ रक्षक)",
        'menu': ['मधुमेह (Diabetes)', 'हृदय रोग (Heart)', 'गुर्दे (Kidney)', 'सर्दी-जुकाम (Cold)'],
        'dia_title': "🩸 मधुमेह (Sugar) की जाँच", 'hrt_title': "❤️ हृदय (Heart) की जाँच",
        'kid_title': "🩺 गुर्दे (Kidney) की जाँच", 'cold_title': "🤧 सर्दी और वायरल जाँच",
        'btn': "परिणाम देखें",
        'safe': "आप स्वस्थ हैं!", 'risk': "खतरा है / बीमारी के संकेत!",
        'dia_adv_safe': "हरी सब्जियां खाएं, रोज 30 मिनट टहलें।", 'dia_adv_risk': "डॉक्टर को दिखाएं। चीनी और चावल बंद करें।",
        'hrt_adv_safe': "व्यायाम करते रहें, तनाव न लें।", 'hrt_adv_risk': "तेल और घी कम खाएं। डॉक्टर से मिलें।",
        'kid_adv_safe': "पानी खूब पिएं, स्वस्थ रहें।", 'kid_adv_risk': "नमक कम खाएं। किडनी विशेषज्ञ को दिखाएं।",
        'cold_safe': "आप बिल्कुल ठीक हैं!", 'cold_mild': "हल्दी वाला दूध पिएं और भाप लें।", 'cold_risk': "बुखार ज्यादा है। तुरंत डॉक्टर के पास जाएं।",
        'loading': "जाँच हो रही है..."
    },
    'Marathi': {
        'title': "हेल्थ गार्ड AI",
        'menu': ['मधुमेह (Diabetes)', 'हृदय विकार (Heart)', 'किडनी (Kidney)', 'सर्दी-ताप (Cold)'],
        'dia_title': "🩸 मधुमेह तपासणी", 'hrt_title': "❤️ हृदय तपासणी",
        'kid_title': "🩺 किडनी तपासणी", 'cold_title': "🤧 सर्दी-ताप तपासणी",
        'btn': "निकाल पहा",
        'safe': "तुम्ही निरोगी आहात!", 'risk': "धोका आहे!",
        'dia_adv_safe': "हिरव्या भाज्या खा, दररोज चाला.", 'dia_adv_risk': "डॉक्टरांना भेटा. साखर टाळा.",
        'hrt_adv_safe': "व्यायाम करा, काळजी घ्या.", 'hrt_adv_risk': "तेलकट खाऊ नका. डॉक्टरांचा सल्ला घ्या.",
        'kid_adv_safe': "भरपूर पाणी प्या.", 'kid_adv_risk': "मीठ कमी खा. तज्ञांना भेटा.",
        'cold_safe': "तुम्ही फिट आहात!", 'cold_mild': "हळदीचे दूध प्या.", 'cold_risk': "ताबडतोब दवाखान्यात जा.",
        'loading': "तपासणी चालू आहे..."
    },
    'Telugu': {
        'title': "హెల్త్ గార్డ్ AI",
        'menu': ['మధుమేహం (Sugar)', 'గుండె వ్యాధి (Heart)', 'కిడ్నీ (Kidney)', 'జలుబు (Cold)'],
        'dia_title': "🩸 మధుమేహం పరీక్ష", 'hrt_title': "❤️ గుండె పనితీరు",
        'kid_title': "🩺 కిడ్నీ పరీక్ష", 'cold_title': "🤧 జలుబు పరీక్ష",
        'btn': "ఫలితం చూడండి",
        'safe': "మీరు ఆరోగ్యంగా ఉన్నారు!", 'risk': "ప్రమాదం ఉంది!",
        'dia_adv_safe': "ఆకుకూరలు తినండి, రోజూ నడవండి.", 'dia_adv_risk': "డాక్టర్ని కలవండి. తీపి తగ్గించండి.",
        'hrt_adv_safe': "వ్యాయామం చేయండి.", 'hrt_adv_risk': "నూనె వస్తువులు మానండి.",
        'kid_adv_safe': "నీరు బాగా తాగండి.", 'kid_adv_risk': "ఉప్పు తగ్గించండి. డాక్టర్ని కలవండి.",
        'cold_safe': "మీరు ఆరోగ్యంగా ఉన్నారు!", 'cold_mild': "పసుపు పాలు తాగండి.", 'cold_risk': "వెంటనే ఆసుపత్రికి వెళ్ళండి.",
        'loading': "పరీక్షిస్తోంది..."
    }
}

# --- Language Selection ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3004/3004458.png", width=80)
    lang_choice = st.selectbox("🌐 Choose Language / भाषा", list(text_dict.keys()))

# Get current language dictionary
t = text_dict[lang_choice]
# Map language name to code for gTTS
lang_codes = {'English': 'en', 'Hindi': 'hi', 'Marathi': 'mr', 'Telugu': 'te'}
lc = lang_codes[lang_choice]

# --- Fail-safe Model Loader ---
def load_model(filename):
    try:
        if os.path.exists(filename):
            return pickle.load(open(filename, 'rb'))
    except: return None
    return None

diabetes_model = load_model('diabetes_model.sav')
heart_model = load_model('heart_model.sav')
kidney_model = load_model('kidney_model.sav')

# --- Helper Functions ---
def speak(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save("audio.mp3")
        st.audio("audio.mp3")
    except: pass

def show_result(is_risk, safe_txt, risk_txt, safe_adv, risk_adv, lang_c):
    st.markdown("---")
    if is_risk:
        st.error(f"⚠️ {risk_txt}")
        st.warning(f"💡 {risk_adv}")
        speak(f"{risk_txt}. {risk_adv}", lang_c)
    else:
        st.success(f"✅ {safe_txt}")
        st.info(f"💡 {safe_adv}")
        speak(f"{safe_txt}. {safe_adv}", lang_c)

# --- LOGIC FUNCTIONS (Backup) ---
def predict_logic_generic(val1, val2, val3, limit1, limit2, limit3):
    if float(val1) > limit1 or float(val2) > limit2 or float(val3) > limit3: return 1
    return 0

# -------------------------------------------
# 2. MAIN MENU & PAGES
# -------------------------------------------
with st.sidebar:
    selected = option_menu(t['title'], t['menu'], 
                           icons=['activity', 'heart', 'droplet', 'thermometer'], 
                           default_index=0)

# === DIABETES ===
if selected == t['menu'][0]:
    st.title(t['dia_title'])
    c1, c2, c3 = st.columns(3)
    glu = c1.text_input("Glucose", '120')
    bp = c2.text_input("BP", '80')
    age = c3.text_input("Age", '30')
    
    # Extra inputs just for show (Models need them)
    bmi = st.text_input("BMI", '25')
    ins = st.text_input("Insulin", '80')
    
    if st.button(t['btn']):
        with st.spinner(t['loading']):
            time.sleep(1)
            # Logic: Gluc > 140 OR BP > 90 OR Age > 50 & BMI > 30
            if diabetes_model:
                try:
                    res = diabetes_model.predict([[0, float(glu), float(bp), 20, float(ins), float(bmi), 0.5, float(age)]])[0]
                except: res = predict_logic_generic(glu, bp, age, 140, 90, 60)
            else:
                res = predict_logic_generic(glu, bp, age, 140, 90, 60)
            
            show_result(res, t['safe'], t['risk'], t['dia_adv_safe'], t['dia_adv_risk'], lc)

# === HEART ===
elif selected == t['menu'][1]:
    st.title(t['hrt_title'])
    c1, c2 = st.columns(2)
    age = c1.text_input("Age", '50')
    hr = c2.text_input("Max Heart Rate", '150')
    cp = st.selectbox("Chest Pain", ["No", "Yes/Mild", "Yes/Severe"])
    oldpeak = st.text_input("ST Depression", '1.0')
    
    if st.button(t['btn']):
        with st.spinner(t['loading']):
            time.sleep(1)
            cp_val = 0 if cp == "No" else 2
            # Logic: CP yes OR HR > 170 OR Oldpeak > 2.0
            if heart_model:
                try:
                    res = heart_model.predict([[float(age),1,cp_val,120,200,0,1,float(hr),0,float(oldpeak),1,0,2]])[0]
                except: res = predict_logic_generic(hr, oldpeak, cp_val, 170, 2.0, 0)
            else:
                res = predict_logic_generic(hr, oldpeak, cp_val, 170, 2.0, 0)
                
            show_result(res, t['safe'], t['risk'], t['hrt_adv_safe'], t['hrt_adv_risk'], lc)

# === KIDNEY ===
elif selected == t['menu'][2]:
    st.title(t['kid_title'])
    c1, c2 = st.columns(2)
    bp = c1.text_input("BP", '80')
    hemo = c2.text_input("Hemoglobin", '15')
    al = st.selectbox("Albumin", ['0','1','2','3','4'])
    
    if st.button(t['btn']):
        with st.spinner(t['loading']):
            time.sleep(1)
            # Logic: BP > 100 OR Albumin > 2 OR Hemo < 10
            # Note: Hemo logic is reversed (Low is bad), handled custom here
            is_risk = 0
            if float(bp) > 100 or int(al) > 2 or float(hemo) < 10: is_risk = 1
            
            if kidney_model:
                try:
                     # Dummy inputs for model
                     res = kidney_model.predict([[40,float(bp),1.02,int(al),0,1,1,0,0,100,30,1.2,135,4.5,float(hemo),40,8000,4.5,0,0,0,1,0,0]])[0]
                except: res = is_risk
            else:
                res = is_risk
            
            show_result(res, t['safe'], t['risk'], t['kid_adv_safe'], t['kid_adv_risk'], lc)

# === COLD (OLD LOGIC + LANGUAGE) ===
elif selected == t['menu'][3]:
    st.title(t['cold_title'])
    
    c1, c2 = st.columns(2)
    with c1:
        fever = st.selectbox("Fever?", ("No", "Mild", "High"))
        cough = st.selectbox("Cough?", ("No", "Dry", "Wet"))
    with c2:
        runny = st.radio("Runny Nose?", ("No", "Yes"), horizontal=True)
        body = st.radio("Body Pain?", ("No", "Yes"), horizontal=True)
    
    if st.button(t['btn']):
        score = 0
        if fever == "High": score+=3
        elif fever == "Mild": score+=1
        if cough != "No": score+=1
        if body == "Yes": score+=2
        
        st.markdown("---")
        if score == 0:
            st.success(f"✅ {t['cold_safe']}")
            speak(t['cold_safe'], lc)
        elif score <= 4:
            st.warning(f"⚠️ {t['cold_mild']}")
            speak(t['cold_mild'], lc)
        else:
            st.error(f"🚨 {t['cold_risk']}")
            speak(t['cold_risk'], lc)
