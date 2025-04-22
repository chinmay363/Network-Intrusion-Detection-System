import ssl
import socket
import threading
from server import start_server as raw_packet_sniffer  

def handle_ssl_connection(connstream):
    while True:
        data = connstream.recv(1024).decode()
        if not data:
            break
        print(f"[SSL MESSAGE] From Client: {data}")

def ssl_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    bindsocket = socket.socket()
    bindsocket.bind(('127.0.0.1', 8443))
    bindsocket.listen(5)
    print("SSL server running on port 8443...")

    while True:
        newsocket, _ = bindsocket.accept()
        connstream = context.wrap_socket(newsocket, server_side=True)
        threading.Thread(target=handle_ssl_connection, args=(connstream,), daemon=True).start()

if __name__ == "__main__":
    threading.Thread(target=ssl_server, daemon=True).start()
    raw_packet_sniffer()  # keep using raw sockets for packet capture

