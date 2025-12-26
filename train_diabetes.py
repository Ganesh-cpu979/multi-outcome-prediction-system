import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
import pickle
import os

# 1. Data Load karo
# (Agar error aaye toh check karna ki file 'Dataset' folder mein hai ya nahi)
dataset = pd.read_csv('Dataset/diabetes.csv')

# 2. Data ko X (Sawaal) aur Y (Jawab) mein baato
X = dataset.drop(columns='Outcome', axis=1)
Y = dataset['Outcome']

# 3. Model Train karo (Machine seekh rahi hai...)
classifier = svm.SVC(kernel='linear')
classifier.fit(X, Y)

# 4. Model ko Save karo (Taaki baar baar train na karna pade)
# Pehle check karo ki 'Models' folder hai ya nahi, nahi toh bana do
if not os.path.exists('Models'):
    os.makedirs('Models')

filename = 'Models/diabetes_model.sav'
pickle.dump(classifier, open(filename, 'wb'))

print("🎉congrats ! model is trained now and saved in 'Models/diabetes_model.sav'.")