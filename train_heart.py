import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
import os

print("⏳ Heart Model training started...")

# 1. Data Load karo
# (Check kar lena file sahi jagah ho)
try:
    heart_data = pd.read_csv('Dataset/heart.csv')
    print("✅ Data found Total records:", len(heart_data))
except:
    print("❌ Error: 'Dataset/heart.csv' not found. Please check where file is located.")
    exit()

# 2. X aur Y alag karo
# Target = 1 (Bimari hai), 0 (Healthy hai)
X = heart_data.drop(columns='target', axis=1)
Y = heart_data['target']

# 3. Model Train karo (Logistic Regression use karenge kyunki ye Yes/No ke liye best hai)
model = LogisticRegression(max_iter=1000)
model.fit(X, Y)

print("🧠 Model is  trained sucessfully!")

# 4. Save karo
if not os.path.exists('Models'):
    os.makedirs('Models')

filename = 'Models/heart_model.sav'
pickle.dump(model, open(filename, 'wb'))

print(f"congrats Heart Model is saved in '{filename}'")