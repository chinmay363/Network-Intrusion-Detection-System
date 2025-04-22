import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the dataset
df = pd.read_csv("C:/Users/Kshirin Shetty/OneDrive/Desktop/Sem 4/NetworkIDS/dataset.csv")

# Drop non-numeric or non-essential features
df = df.drop(columns=["frame.number", "frame.time", "eth.src", "eth.dst", "ip.src", "ip.dst"])

# Encode the label
label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["normality"])  # normality → 0 or 1
df = df.drop(columns=["normality"])

# Separate features and label
X = df.drop(columns=["label"])
y = df["label"]

# Train the Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# Save the model and label encoder
joblib.dump(clf, "model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("Model and encoder saved!")
