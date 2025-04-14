import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Sample dataset
df = pd.read_csv(r"D:\AIDI Sem2\AI_in_EnterpriseSystems\Final_project\visa-smart-system\data\data.csv")

X = df[['age', 'income', 'nationality_code', 'travel_history']]
y = df['visa_approved']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved.")
