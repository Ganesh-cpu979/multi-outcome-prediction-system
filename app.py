import streamlit as st
from streamlit_option_menu import option_menu
import pickle
from gtts import gTTS
import os
import random

# -------------------------------------------
# 1. Models Load karna (Safe Mode)
# -------------------------------------------
models_dir = '.'

def load_model(filename):
    try:
        path = f'{models_dir}/{filename}'
        return pickle.load(open(path, 'rb'))
    except:
        return None

diabetes_model = load_model('diabetes_model.sav')
heart_model = load_model('heart_model.sav')
kidney_model = load_model('kidney_model.sav')

# -------------------------------------------
# 2. Page Setup & LANGUAGE DICTIONARY 🗣️
# -------------------------------------------
st.set_page_config(page_title="Multi Outcome Prediction", layout="wide", page_icon="🏥")

# --- CUSTOM CSS FOR TOP NAVBAR ---
st.markdown("""
<style>
    .nav-link { font-size: 18px !important; text-align: center; margin: 0px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Language / भाषा")
    lang_choice = st.selectbox("Choose Language:", 
                               ('English', 'Hindi', 'Marathi', 'Telugu'))

lang_code_map = {'English': 'en', 'Hindi': 'hi', 'Marathi': 'mr', 'Telugu': 'te'}
selected_lang_code = lang_code_map[lang_choice]

# Function for Text-to-Speech
def speak(text_to_speak, lang_code):
    try:
        tts = gTTS(text=text_to_speak, lang=lang_code)
        tts.save("temp_audio.mp3")
        st.audio("temp_audio.mp3")
    except:
        st.error("Audio Error: Internet Connection Required.")

# --- TRANSLATION DICTIONARY ---
text = {
    'English': {
        'sidebar_title': "Prediction Menu",
        'opt_home': "Home Page",
        'opt_diabetes': "Diabetes Prediction",
        'opt_heart': "Heart Disease",
        'opt_kidney': "Kidney Disease",
        'opt_cold': "Viral/Cold Check",
        'btn_result': "Get Result & Advice", 'btn_audio': "🔊 Listen",
        'advice_title': "💡 AI Suggestions & Remedies:",
        
        # Diabetes
        'dia_title': "🩸 Diabetes Prediction",
        'dia_safe': "Result: Healthy (No Diabetes)", 
        'dia_risk': "Result: High Risk of Diabetes",
        'dia_sug_safe': "• Eat green vegetables & fruits.\n• Walk 30 mins daily.\n• Drink 3L water.",
        'dia_sug_risk': "• Consult a Doctor immediately.\n• Avoid Sugar, Rice, Potatoes.\n• Remedy: Eat soaked Methi seeds empty stomach.",

        # Heart
        'hrt_title': "❤️ Heart Disease Prediction",
        'hrt_safe': "Result: Healthy Heart", 
        'hrt_risk': "Result: Heart Disease Detected",
        'hrt_sug_safe': "• Do Cardio exercises (Run/Swim).\n• Eat walnuts and flaxseeds.\n• Manage stress.",
        'hrt_sug_risk': "• Visit Cardiologist ASAP.\n• Stop Oil, Ghee, and Butter completely.\n• Remedy: Drink Bottle Gourd (Lauki) Juice.",

        # Kidney
        'kid_title': "🩺 Kidney Disease Prediction",
        'kid_safe': "Result: Healthy Kidneys", 
        'kid_risk': "Result: Kidney Issue Detected",
        'kid_sug_safe': "• Stay hydrated.\n• Don't hold urine for long.\n• Limit painkillers.",
        'kid_sug_risk': "• Consult Nephrologist.\n• Low Salt & Low Protein diet.\n• Avoid Bananas & Oranges (High Potassium).",

        # Cold
        'cold_title': "🤧 Viral & Cold Check",
        'cold_safe': "Result: You are Healthy!", 
        'cold_mild': "Result: Viral Fever / Cold",
        'cold_risk': "Result: High Infection Risk / Flu",
        'cold_sug_safe': "• Keep immune system strong.\n• Eat Vitamin C fruits.",
        'cold_sug_mild': "• Drink Turmeric Milk (Haldi Doodh).\n• Take Steam inhalation.\n• Gargle with salt water.",
        'cold_sug_risk': "• Go to Hospital immediately.\n• Isolate yourself.\n• Monitor Oxygen levels.",

        # Common Labels
        'age': "Age", 'bp': "Blood Pressure", 'gender': "Gender", 'male': "Male", 'female': "Female",
        'yes': "Yes", 'no': "No", 'gluc': "Glucose", 'insu': "Insulin", 'cp': "Chest Pain", 
        'chol': "Cholesterol", 'al': "Albumin", 'hemo': "Hemoglobin"
    },

    'Hindi': {
        'sidebar_title': "मुख्य मेनू",
        'opt_home': "🏠 होम पेज",
        'opt_diabetes': "मधुमेह (Sugar)", 'opt_heart': "हृदय रोग (Heart)", 'opt_kidney': "गुर्दे (Kidney)", 'opt_cold': "सर्दी-जुकाम",
        'btn_result': "परिणाम और सलाह", 'btn_audio': "🔊 सुनें",
        'advice_title': "💡 AI सलाह और घरेलू उपाय:",

        'dia_title': "🩸 मधुमेह (Sugar) की जाँच",
        'dia_safe': "परिणाम: स्वस्थ (शुगर नहीं है)", 
        'dia_risk': "परिणाम: शुगर (Diabetes) का खतरा है",
        'dia_sug_safe': "• हरी सब्जियां और फल खाएं।\n• रोज 30 मिनट टहलें।\n• दिन में 3 लीटर पानी पिएं।",
        'dia_sug_risk': "• तुरंत डॉक्टर से मिलें।\n• चीनी, चावल और आलू बंद करें।\n• उपाय: सुबह भीगे हुए मेथी दाने खाएं।",

        'hrt_title': "❤️ हृदय रोग (Heart) की जाँच",
        'hrt_safe': "परिणाम: आपका दिल स्वस्थ है", 
        'hrt_risk': "परिणाम: हृदय रोग के संकेत हैं",
        'hrt_sug_safe': "• कार्डियो व्यायाम (दौड़ना/तैरना) करें।\n• अखरोट खाएं।\n• तनाव (Stress) कम लें।",
        'hrt_sug_risk': "• तुरंत कार्डियोलॉजिस्ट के पास जाएं।\n• तेल, घी और मक्खन पूरी तरह बंद करें।\n• उपाय: लौकी का जूस पिएं।",

        'kid_title': "🩺 गुर्दे (Kidney) की जाँच",
        'kid_safe': "परिणाम: गुर्दे स्वस्थ हैं", 
        'kid_risk': "परिणाम: गुर्दे में समस्या हो सकती है",
        'kid_sug_safe': "• पानी खूब पिएं।\n• पेशाब ज्यादा देर न रोकें।\n• पेनकिलर दवा कम लें।",
        'kid_sug_risk': "• डॉक्टर (Nephrologist) को दिखाएं।\n• नमक और प्रोटीन कम खाएं।\n• केला और संतरा न खाएं।",

        'cold_title': "🤧 सर्दी और वायरल जाँच",
        'cold_safe': "परिणाम: आप बिल्कुल स्वस्थ हैं!", 
        'cold_mild': "परिणाम: वायरल बुखार / सर्दी है",
        'cold_risk': "परिणाम: फ्लू या इन्फेक्शन का खतरा",
        'cold_sug_safe': "• अपनी इम्युनिटी मजबूत रखें।\n• विटामिन सी वाले फल खाएं।",
        'cold_sug_mild': "• हल्दी वाला दूध पिएं।\n• भाप (Steam) लें।\n• नमक के पानी से गरारे करें।",
        'cold_sug_risk': "• तुरंत अस्पताल जाएं।\n• सांस पर ध्यान दें।",
        
        'age': "आयु", 'bp': "रक्तचाप", 'gender': "लिंग", 'male': "पुरुष", 'female': "महिला",
        'yes': "हाँ", 'no': "नहीं", 'gluc': "ग्लूकोज", 'insu': "इंसुलिन", 'cp': "छाती में दर्द", 
        'chol': "कोलेस्ट्रॉल", 'al': "एल्ब्यूमिन", 'hemo': "हीमोग्लोबिन"
    },
    'Marathi': {
        'sidebar_title': "मुख्य मेनू", 'opt_home': "🏠 मुख्य पृष्ठ",
        'opt_diabetes': "मधुमेह", 'opt_heart': "हृदय विकार", 'opt_kidney': "किडनी विकार", 'opt_cold': "सर्दी-ताप",
        'btn_result': "निकाल आणि सल्ला", 'btn_audio': "🔊 ऐका", 'advice_title': "💡 AI सल्ला आणि उपाय:",
        
        'dia_title': "🩸 मधुमेह तपासणी", 'dia_safe': "निरोगी (शुगर नाही)", 'dia_risk': "शुगरचा धोका आहे",
        'dia_sug_safe': "• हिरव्या पालेभाज्या खा.\n• दररोज चाला.", 'dia_sug_risk': "• डॉक्टरांना भेटा.\n• साखर, भात टाळा.\n• उपाय: मेथीचे दाणे खा.",
        
        'hrt_title': "❤️ हृदय तपासणी", 'hrt_safe': "हृदय निरोगी आहे", 'hrt_risk': "हृदय विकाराचा धोका",
        'hrt_sug_safe': "• व्यायाम करा.\n• ताण घेऊ नका.", 'hrt_sug_risk': "• डॉक्टरांना भेटा.\n• तेलकट खाणे बंद करा.\n• उपाय: दुधी भोपळ्याचा रस प्या.",

        'kid_title': "🩺 किडनी तपासणी", 'kid_safe': "किडनी निरोगी आहे", 'kid_risk': "किडनी विकाराचा धोका",
        'kid_sug_safe': "• भरपूर पाणी प्या.", 'kid_sug_risk': "• डॉक्टरांचा सल्ला घ्या.\n• मीठ कमी खा.",

        'cold_title': "🤧 सर्दी तपासणी", 'cold_safe': "निरोगी!", 'cold_mild': "सर्दी/ताप आहे", 'cold_risk': "संसर्ग धोका",
        'cold_sug_safe': "• काळजी घ्या.", 'cold_sug_mild': "• हळदीचे दूध प्या.\n• वाफ घ्या.", 'cold_sug_risk': "• हॉस्पिटलला जा.",

        'age': "वय", 'bp': "रक्तदाब", 'gender': "लिंग", 'male': "पुरुष", 'female': "स्त्री", 'yes': "हो", 'no': "नाही",
        'gluc': "ग्लुकोज", 'insu': "इन्सुलिन", 'cp': "छातीत दुखणे", 'chol': "कोलेस्ट्रॉल", 'al': "अल्ब्युमिन", 'hemo': "हिमोग्लोबिन"
    },
    'Telugu': {
        'sidebar_title': "వ్యాధి నిర్ధారణ", 'opt_home': "🏠 హోమ్ పేజీ",
        'opt_diabetes': "మధుమేహం", 'opt_heart': "గుండె వ్యాధి", 'opt_kidney': "కిడ్నీ వ్యాధి", 'opt_cold': "జలుబు",
        'btn_result': "ఫలితం మరియు సలహా", 'btn_audio': "🔊 వినండి", 'advice_title': "💡 సలహాలు మరియు చిట్కాలు:",
        
        'dia_title': "🩸 మధుమేహం", 'dia_safe': "ఆరోగ్యం (Sugar లేదు)", 'dia_risk': "Sugar ప్రమాదం",
        'dia_sug_safe': "• ఆకుకూరలు తినండి.\n• రోజూ నడవండి.", 'dia_sug_risk': "• డాక్టరును కలవండి.\n• తీపి, అన్నం తగ్గించండి.\n• చిట్కా: మెంతులు తినండి.",
        
        'hrt_title': "❤️ గుండె వ్యాధి", 'hrt_safe': "గుండె ఆరోగ్యం", 'hrt_risk': "గుండె వ్యాధి ప్రమాదం",
        'hrt_sug_safe': "• వ్యాయామం చేయండి.", 'hrt_sug_risk': "• డాక్టరును కలవండి.\n• నూనె వస్తువులు మానండి.\n• చిట్కా: సొరకాయ రసం తాగండి.",

        'kid_title': "🩺 కిడ్నీ వ్యాధి", 'kid_safe': "కిడ్నీలు ఆరోగ్యం", 'kid_risk': "కిడ్నీ సమస్య",
        'kid_sug_safe': "• నీరు తాగండి.", 'kid_sug_risk': "• డాక్టరును కలవండి.\n• ఉప్పు తగ్గించండి.",

        'cold_title': "🤧 జలుబు", 'cold_safe': "ఆరోగ్యం!", 'cold_mild': "జ్వరం/జలుబు", 'cold_risk': "ఫ్లూ ప్రమాదం",
        'cold_sug_safe': "• జాగ్రత్తగా ఉండండి.", 'cold_sug_mild': "• పసుపు పాలు తాగండి.\n• ఆవిరి పట్టండి.", 'cold_sug_risk': "• ఆసుపత్రికి వెళ్ళండి.",

        'age': "వయస్సు", 'bp': "BP", 'gender': "లింగం", 'male': "పురుషుడు", 'female': "స్త్రీ", 'yes': "అవును", 'no': "కాదు",
        'gluc': "గ్లూకోజ్", 'insu': "ఇన్సులిన్", 'cp': "ఛాతీ నొప్పి", 'chol': "కొలెస్ట్రాల్", 'al': "అల్బుమిన్", 'hemo': "హీమోగ్లోబిన్"
    }
}

t = text[lang_choice]

# Sidebar Menu
with st.sidebar:
    selected = option_menu(t['sidebar_title'],
                           [t['opt_home'], t['opt_diabetes'], t['opt_heart'], t['opt_kidney'], t['opt_cold']],
                           icons=['house', 'activity', 'heart', 'droplet', 'thermometer-half'],
                           default_index=0)

# ================= 0. HOME PAGE WITH NAVIGATION =================
if selected == t['opt_home']:
    
    # --- Top Navigation Bar ---
    selected_nav = option_menu(None, ["Home", "About Us", "Services", "Health Tips"], 
                               icons=['house', 'info-circle', 'gear', 'lightbulb'], 
                               menu_icon="cast", default_index=0, orientation="horizontal",
                               styles={
                                   "container": {"padding": "0!important", "background-color": "#fafafa"},
                                   "icon": {"color": "orange", "font-size": "18px"}, 
                                   "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                   "nav-link-selected": {"background-color": "#02ab21"},
                               })

    # 1. HOME TAB (Updated Image & Fixed Warning)
    if selected_nav == "Home":
        st.markdown("<h1 style='text-align: center; color: #02ab21;'>🏥 Multi Outcome Prediction</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Your Intelligent Health Companion | Powered by Machine Learning</h4>", unsafe_allow_html=True)
        
        # FIX: 'use_column_width' removed, 'use_container_width' added.
        # FIX: New Reliable Image URL (Unsplash)
        st.image("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d", use_container_width=True)
        
        st.info("👈 Select a disease from the Sidebar to start prediction.")

    # 2. ABOUT US TAB
    elif selected_nav == "About Us":
        st.header("👥 About Us")
        st.write("""
        **Multi Outcome Prediction System** is a final year diploma project designed to bridge the gap between technology and healthcare in rural areas.
        
        **Our Mission:**
        To provide a free, accurate, and accessible health screening tool for everyone.
        
        **Developed By:**
        * **J. Ganesh** (Team Leader)
        * **Sai ram**
        * **Navya Sri**
        * **Manish**
        * **Mrigank**
        * **Akshitha**
        """)

    # 3. SERVICES TAB
    elif selected_nav == "Services":
        st.header("🛠️ Our Services")
        col1, col2 = st.columns(2)
        with col1:
            st.success("🩸 **Diabetes Check**")
            st.write("Instant sugar level risk analysis using SVM.")
            st.success("❤️ **Heart Check**")
            st.write("Cardiovascular health prediction.")
        with col2:
            st.success("🩺 **Kidney Check**")
            st.write("Renal health monitoring system.")
            st.success("🗣️ **Voice Support**")
            st.write("Results in Hindi, Marathi, Telugu & English.")

    # 4. TIPS TAB (RANDOMIZED)
    elif selected_nav == "Health Tips":
        st.header("🥗 Daily Health Tips (Updated)")
        
        all_tips = [
            "Drink at least 3-4 liters of water daily to stay hydrated.",
            "Sleep for 7-8 hours every night for better mental health.",
            "Reduce sugar and salt intake to control blood pressure.",
            "Walk for 30 minutes every day to keep your heart healthy.",
            "Eat more fiber-rich foods like oats, apples, and beans.",
            "Avoid processed and junk food to prevent obesity.",
            "Practice meditation for 10 minutes daily to reduce stress.",
            "Wash your hands frequently to avoid viral infections.",
            "Eat a handful of nuts (walnuts/almonds) daily.",
            "Limit screen time before bed for better sleep quality.",
            "Do not skip breakfast; it boosts your metabolism.",
            "Limit caffeine intake after 6 PM.",
            "Include Vitamin C (Oranges, Lemons) in your diet for immunity.",
            "Maintain a healthy body weight to reduce disease risk.",
            "Avoid smoking and alcohol for a healthy liver and lungs."
        ]
        
        random_tips = random.sample(all_tips, 4)
        
        for i, tip in enumerate(random_tips):
            st.warning(f"**Tip {i+1}:** {tip}")

        if st.button("🔄 Load New Tips"):
            st.rerun()

    st.markdown("---")
    st.caption("© 2026 Multi Outcome Prediction | Final Year Project")

# ================= 1. DIABETES PAGE =================
elif selected == t['opt_diabetes']:
    st.title(t['dia_title'])
    st.info("ℹ️ Please enter values below / कृपया नीचे जानकारी भरें")

    gender = st.radio(t['gender'], [t['male'], t['female']], horizontal=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Pregnancies = st.text_input("Pregnancies", '') if gender == t['female'] else '0'
        SkinThickness = st.text_input("Skin Thickness", '')
        fam = st.selectbox("Family History", ("No", "Yes"))
        DPF = 0.1 if fam == "No" else 0.8
    with col2:
        Glucose = st.text_input(t['gluc'], '')
        insu_qn = st.radio("Insulin?", (t['no'], t['yes']), horizontal=True)
        Insulin = st.text_input(t['insu'], '') if insu_qn == t['yes'] else '0'
        Age = st.text_input(t['age'], '')
    with col3:
        BloodPressure = st.text_input(t['bp'], '')
        BMI = st.text_input("BMI", '')

    if st.button(t['btn_result']):
        if diabetes_model:
            try:
                user_input = [float(Pregnancies), float(Glucose), float(BloodPressure), 
                              float(SkinThickness), float(Insulin), float(BMI), DPF, float(Age)]
                
                pred = diabetes_model.predict([user_input])
                st.markdown("---")
                msg = ""
                
                if pred[0] == 0:
                    st.balloons()
                    st.success(t['dia_safe'])
                    st.info(f"**{t['advice_title']}**\n\n{t['dia_sug_safe']}")
                    msg = f"{t['dia_safe']}... {t['dia_sug_safe']}"
                else:
                    st.error(t['dia_risk'])
                    st.progress(90)
                    st.warning(f"**{t['advice_title']}**\n\n{t['dia_sug_risk']}")
                    msg = f"{t['dia_risk']}... {t['dia_sug_risk']}"
                
                st.session_state['aud_dia'] = msg
            except ValueError:
                st.warning("⚠️ Please fill all fields / कृपया सभी बॉक्स भरें")
            except Exception as e:
                st.error(f"Error: {e}")
        else: st.error("Diabetes Model not found")
    
    if 'aud_dia' in st.session_state and st.button(t['btn_audio']): speak(st.session_state['aud_dia'], selected_lang_code)

# ================= 2. HEART PAGE =================
elif selected == t['opt_heart']:
    st.title(t['hrt_title'])
    st.info("ℹ️ Please enter values below / कृपया नीचे जानकारी भरें")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.text_input(t['age'], '')
        sex = st.selectbox(t['gender'], (t['male'], t['female']))
        sex_val = 1 if sex == t['male'] else 0
        cp = st.selectbox(t['cp'], ("Typical", "Atypical", "Non-anginal", "Asymptomatic"))
        cp_val = 0 if cp=="Typical" else (1 if cp=="Atypical" else (2 if cp=="Non-anginal" else 3))
        trestbps = st.text_input(t['bp'], '')
    with col2:
        chol = st.text_input(t['chol'], '')
        fbs = st.radio("Sugar > 120?", (t['no'], t['yes']), horizontal=True)
        fbs_val = 1 if fbs == t['yes'] else 0
        restecg = st.selectbox("ECG", ("Normal", "Abnormal"))
        restecg_val = 0 if restecg=="Normal" else 1
        thalach = st.text_input("Max Heart Rate", '')
    with col3:
        exang = st.radio("Exercise Pain?", (t['no'], t['yes']), horizontal=True)
        exang_val = 1 if exang == t['yes'] else 0
        oldpeak = st.text_input("ST Depression", '')
        slope = st.selectbox("Slope", ("Upsloping", "Flat", "Downsloping"))
        slope_val = 0 if slope=="Upsloping" else (1 if slope=="Flat" else 2)
        ca = st.selectbox("Major Vessels", ('0','1','2','3'))
        thal = st.selectbox("Thal", ("Normal", "Fixed", "Reversable"))
        thal_val = 1 if thal=="Normal" else (2 if thal=="Fixed" else 3)

    if st.button(t['btn_result']):
        if heart_model:
            try:
                user_input = [float(age), sex_val, cp_val, float(trestbps), float(chol), 
                              fbs_val, restecg_val, float(thalach), exang_val, float(oldpeak), 
                              slope_val, float(ca), thal_val]
                pred = heart_model.predict([user_input])
                st.markdown("---")
                msg = ""
                
                if pred[0] == 0:
                    st.balloons(); st.success(t['hrt_safe'])
                    st.info(f"**{t['advice_title']}**\n\n{t['hrt_sug_safe']}")
                    msg = f"{t['hrt_safe']}... {t['hrt_sug_safe']}"
                else:
                    st.error(t['hrt_risk']); st.progress(90)
                    st.warning(f"**{t['advice_title']}**\n\n{t['hrt_sug_risk']}")
                    msg = f"{t['hrt_risk']}... {t['hrt_sug_risk']}"
                    
                st.session_state['aud_hrt'] = msg
            except ValueError:
                st.warning("⚠️ Please fill all fields / कृपया सभी बॉक्स भरें")
            except: st.warning("Check Inputs")
        else: st.error("Heart Model not found")

    if 'aud_hrt' in st.session_state and st.button(t['btn_audio']): speak(st.session_state['aud_hrt'], selected_lang_code)

# ================= 3. KIDNEY PAGE =================
elif selected == t['opt_kidney']:
    st.title(t['kid_title'])
    st.info("ℹ️ Please enter values below / कृपया नीचे जानकारी भरें")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.text_input(t['age'], '')
        bp = st.text_input(t['bp'], '')
        al = st.selectbox(t['al'], ('0', '1', '2', '3', '4', '5'))
    with col2:
        su = st.selectbox("Sugar (0-5)", ('0', '1', '2', '3', '4', '5'))
        rbc = st.radio("RBC", ("Normal", "Abnormal"), horizontal=True)
        rbc_val = 1 if rbc == "Normal" else 0
        pc = st.radio("Pus Cell", ("Normal", "Abnormal"), horizontal=True)
        pc_val = 1 if pc == "Normal" else 0
    with col3:
        hemo = st.text_input(t['hemo'], '')

    if st.button(t['btn_result']):
        if kidney_model:
            try:
                user_input = [float(age), float(bp), float(al), float(su), rbc_val, pc_val, float(hemo)]
                pred = kidney_model.predict([user_input])
                st.markdown("---")
                msg = ""
                
                if pred[0] == 0: 
                    st.balloons(); st.success(t['kid_safe'])
                    st.info(f"**{t['advice_title']}**\n\n{t['kid_sug_safe']}")
                    msg = f"{t['kid_safe']}... {t['kid_sug_safe']}"
                else:
                    st.error(t['kid_risk']); st.progress(90)
                    st.warning(f"**{t['advice_title']}**\n\n{t['kid_sug_risk']}")
                    msg = f"{t['kid_risk']}... {t['kid_sug_risk']}"
                
                st.session_state['aud_kid'] = msg
            except ValueError:
                st.warning("⚠️ Please fill all fields / कृपया सभी बॉक्स भरें")
            except Exception as e: st.warning(f"Error: {e}")
        else: st.error("Kidney Model not found")

    if 'aud_kid' in st.session_state and st.button(t['btn_audio']): speak(st.session_state['aud_kid'], selected_lang_code)

# ================= 4. COLD/VIRAL PAGE =================
elif selected == t['opt_cold']:
    st.title(t['cold_title'])
    col1, col2 = st.columns(2)
    with col1:
        fever = st.selectbox("Fever?", ("No", "Mild", "High"))
        cough = st.selectbox("Cough?", ("No", "Dry", "Wet"))
    with col2:
        runny = st.radio("Runny Nose?", (t['no'], t['yes']), horizontal=True)
        body = st.radio("Body Pain?", (t['no'], t['yes']), horizontal=True)
        breath = st.radio("Breathing Issue?", (t['no'], t['yes']), horizontal=True)
    
    if st.button(t['btn_result']):
        score = 0
        if fever == "High": score+=3
        elif fever == "Mild": score+=1
        if cough != "No": score+=1
        if body == t['yes']: score+=2
        if breath == t['yes']: score+=5
        
        st.markdown("---")
        msg = ""
        if score == 0:
            st.balloons(); st.success(t['cold_safe'])
            st.info(f"**{t['advice_title']}**\n\n{t['cold_sug_safe']}")
            msg = f"{t['cold_safe']}... {t['cold_sug_safe']}"
        elif score <= 4:
            st.warning(t['cold_mild'])
            st.info(f"**{t['advice_title']}**\n\n{t['cold_sug_mild']}")
            msg = f"{t['cold_mild']}... {t['cold_sug_mild']}"
        else:
            st.error(t['cold_risk']); st.progress(90)
            st.warning(f"**{t['advice_title']}**\n\n{t['cold_sug_risk']}")
            msg = f"{t['cold_risk']}... {t['cold_sug_risk']}"
            
        st.session_state['aud_cold'] = msg

    if 'aud_cold' in st.session_state and st.button(t['btn_audio']): speak(st.session_state['aud_cold'], selected_lang_code)

