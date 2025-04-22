# Intrusion Detection System (IDS) using Raw Sockets and Random Forest Classifier

## Overview

This project implements a Network Intrusion Detection System (NIDS) that captures network traffic using raw sockets and employs a Random Forest machine learning classifier to identify malicious activity. The system is trained on the ["IoT Device Network Logs" dataset](https://www.kaggle.com/datasets/speedwall10/iot-device-network-logs) from Kaggle.

### Project Goals

- Capture raw network packets directly from a network interface.
- Extract relevant features from the captured network traffic.
- Utilize a Random Forest classifier to distinguish between normal and malicious network behavior.
- Provide a basic alerting mechanism for detected intrusions.

---

## Features

- Real-time network packet capture using raw sockets
- Secure client-server communication using SSL/TLS
- ML-powered anomaly detection using a trained Random Forest Classifier
- Feature extraction from raw IP/TCP headers
- Lightweight and modular design for easy experimentation

---

## How It Works

### 1. Client

- Captures raw packets using `socket.AF_PACKET` (Linux) or `socket.IPPROTO_IP` (Windows).
- Extracts key features: frame length, IP length, protocol, TCP ports, etc.
- Sends this data securely to the server via SSL-encrypted socket.

### 2. Server

- Listens for incoming connections using SSL.
- Loads a pre-trained Random Forest model and a Label Encoder.
- Classifies incoming packet data as `'normal'` or `'anomalous'`.
- Logs or returns results to the client.

---

## Machine Learning Component

- **Training Script**: `train_model.py`  
  Trains a Random Forest model on labeled packet data.  
  Saves the model (`model.pkl`) and label encoder (`label_encoder.pkl`).

- **Prediction Script**: `predict_packet.py`  
  Loads the trained model.  
  Predicts labels for new feature vectors in real-time.

---

## Project Structure
├── client.py               # Captures packets & sends features to server  
├── ssl_server.py           # Secure server that predicts using ML model  
├── train_model.py          # Trains the Random Forest model  
├── predict_packet.py       # Performs live prediction  
├── dataset.csv             # Labeled training data for model  
├── model.pkl               # Trained Random Forest model  
├── label_encoder.pkl       # Encodes/decodes labels  
├── cert.pem, key.pem       # SSL certificate & private key
