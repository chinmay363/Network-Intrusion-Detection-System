import socket
import struct
import random
import time
import ssl
import os

def build_ip_header(src_ip, dst_ip, proto, total_length):
    return struct.pack('!BBHHHBBH4s4s',
                       69, 0, total_length, 54321, 0, 64, proto, 0,
                       socket.inet_aton(src_ip), socket.inet_aton(dst_ip))

def build_tcp_header(src_port, dst_port, flags, payload=b''):
    seq = 0
    ack_seq = 0
    doff = 5
    window = socket.htons(5840)
    check = 0
    urg_ptr = 0

    tcp_offset_res = (doff << 4) + 0
    tcp_flags = flags

    return struct.pack('!HHLLBBHHH',
                       src_port, dst_port, seq, ack_seq,
                       tcp_offset_res, tcp_flags, window, check, urg_ptr) + payload

def send_packet(ip_header, tcp_header, dst_ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    packet = ip_header + tcp_header
    s.sendto(packet, (dst_ip, 0))

def simulate_syn_flood(src_ip, dst_ip):
    src_port = random.randint(1024, 65535)
    dst_port = 80
    ip_header = build_ip_header(src_ip, dst_ip, socket.IPPROTO_TCP, 40)
    tcp_header = build_tcp_header(src_port, dst_port, 0x02)  # SYN
    send_packet(ip_header, tcp_header, dst_ip)

def simulate_port_scan(src_ip, dst_ip):
    src_port = random.randint(1024, 65535)
    dst_port = random.randint(1, 1024)
    ip_header = build_ip_header(src_ip, dst_ip, socket.IPPROTO_TCP, 40)
    tcp_header = build_tcp_header(src_port, dst_port, 0x02)  # SYN
    send_packet(ip_header, tcp_header, dst_ip)

def simulate_malformed_packet(src_ip, dst_ip):
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            0x00, 0x00, 0x00, 0x00, 0, 0, 0, 0,
                            socket.inet_aton(src_ip), socket.inet_aton(dst_ip))
    payload = b'\x00\xff\x00\xff' * 10
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    s.sendto(ip_header + payload, (dst_ip, 0))

def send_normal_packet(src_ip, dst_ip):
    src_port = random.randint(1024, 65535)
    dst_port = 80
    payload = b'HelloServer'
    ip_header = build_ip_header(src_ip, dst_ip, socket.IPPROTO_TCP, 40 + len(payload))
    tcp_header = build_tcp_header(src_port, dst_port, 0x18, payload)  # PSH + ACK
    send_packet(ip_header, tcp_header, dst_ip)

def send_ssl_signal(message):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection(('127.0.0.1', 8443)) as sock:
            with context.wrap_socket(sock, server_hostname='localhost') as ssock:
                ssock.sendall(message.encode())
    except Exception as e:
        print(f"[SSL ERROR] {e}")

def send_attack_packets(count):
    src_ip = "127.0.0.1"
    dst_ip = "127.0.0.1"

    attack_types = ["syn_flood", "port_scan", "malformed", "normal"]
    for _ in range(count):
        attack = random.choice(attack_types)
        print(f"Simulating: {attack}")
        send_ssl_signal(f"Sent: {attack}") 
        if attack == "syn_flood":
            simulate_syn_flood(src_ip, dst_ip)
        elif attack == "port_scan":
            simulate_port_scan(src_ip, dst_ip)
        elif attack == "malformed":
            simulate_malformed_packet(src_ip, dst_ip)
        elif attack == "normal":
            send_normal_packet(src_ip, dst_ip)
        time.sleep(0.1)

def spawn_another_pair():
    os.system('gnome-terminal -- bash -c "python3 ssl_server.py; exec bash"')
    os.system('gnome-terminal -- bash -c "python3 client.py; exec bash"')

def main():
    while True:
        print("\nClient Menu:")
        print("1. Create another client-server pair")
        print("2. Send random packets (attack/normal)")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            spawn_another_pair()
        elif choice == "2":
            count = int(input("How many packets to send? "))
            send_attack_packets(count)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

