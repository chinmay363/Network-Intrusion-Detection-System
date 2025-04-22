import joblib
import numpy as np

# Load the model and label encoder
clf = joblib.load("model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Define the prediction function
def predict_from_features(features_list):
    """
    features_list: [frame.len, ip.proto, ip.len, tcp.len, tcp.srcport, tcp.dstport, value]
    """
    features_array = np.array(features_list).reshape(1, -1)
    pred = clf.predict(features_array)[0]
    label = label_encoder.inverse_transform([pred])[0]
    return label
