import socket
import struct
import pandas as pd
import warnings

from predict_packet import predict_from_features

def extract_features(packet):
    try:
        ip_header = packet[14:34]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

        frame_len = len(packet)
        ip_proto = iph[6]
        ip_len = iph[2]

        if ip_proto == 6:  # TCP
            tcp_header = packet[34:54]
            tcph = struct.unpack('!HHLLBBHHH', tcp_header)
            src_port = tcph[0]
            dst_port = tcph[1]
            tcp_len = (tcph[4] >> 4) * 4
        else:
            src_port = dst_port = tcp_len = 0

        value = sum(packet) % 1024 

        features = [frame_len, ip_proto, ip_len, tcp_len, src_port, dst_port, value]
        columns = ['frame_len', 'ip_proto', 'ip_len', 'tcp_len', 'src_port', 'dst_port', 'value']
        df = pd.DataFrame([features], columns=columns)
        return df
    except:
        return None

def start_server():
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    print("Server is listening for packets...")

    while True:
        packet, _ = s.recvfrom(65565)
        features = extract_features(packet)

        if not features.empty:
            warnings.filterwarnings("ignore", category=UserWarning, message="X does not have valid feature names")
            result = predict_from_features(features)
            print(f"Prediction: {result}")

if __name__ == "__main__":
    start_server()
