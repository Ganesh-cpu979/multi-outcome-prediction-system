import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os

print("⏳ Kidney Model training started...")

# 1. Data Load karo
try:
    data = pd.read_csv('Dataset/kidney.csv')
    print("✅ Data found!")
except:
    print("❌ Error: File not found ! Check if kidney.csv prenent in 'Dataset' folder .")
    exit()

# 2. Data Cleaning (Text ko Number banana)
# classification: ckd = 1, notckd = 0
data['classification'] = data['classification'].map({'ckd': 1, 'notckd': 0})

# rbc aur pc: normal = 1, abnormal = 0
data['rbc'] = data['rbc'].map({'normal': 1, 'abnormal': 0})
data['pc'] = data['pc'].map({'normal': 1, 'abnormal': 0})

# 3. Training ke liye tayyar
X = data[['age', 'bp', 'al', 'su', 'rbc', 'pc', 'hemo']]
Y = data['classification']

# 4. Model Train
print("🧠 Model is training....")
model = LogisticRegression(max_iter=1000)
model.fit(X, Y)

# 5. Save Model
if not os.path.exists('Models'):
    os.makedirs('Models')

filename = 'Models/kidney_model.sav'
pickle.dump(model, open(filename, 'wb'))

print(f"🎉 congrats ! Kidney Model is saved in'{filename}'.")