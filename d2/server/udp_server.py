import socket
import threading
import time
from cryptography.fernet import Fernet
from config import *
from state import nodes, event_counts, last_seq, lock
from database import insert_event

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

cipher = Fernet(KEY)

print("UDP Monitoring Server Running...")


def receiver():
    while True:
        data, addr = sock.recvfrom(4096)

        try:
            decrypted = cipher.decrypt(data).decode()
            node, seq, ts, event, metric, value = decrypted.split("|")

            seq = int(seq)
            ts = int(ts)

        except Exception as e:
            print("Invalid packet:", e)
            continue

        with lock:
            # Packet loss detection
            if node in last_seq and seq != last_seq[node] + 1:
                print(f"[LOSS] Packet loss from {node}")

            last_seq[node] = seq

            severity = EVENT_TYPES.get(event, "UNKNOWN")

            nodes[node] = {
                "ip": addr[0],
                "last_seen": ts,
                "event": (event, metric, value, severity),
            }

            event_counts[event] += 1

            insert_event(node, ts, event, metric, value)

        print(f"[RECV] {node} -> {event} ({metric}={value})")

        # ACK (basic reliability)
        sock.sendto(f"ACK|{node}|{seq}".encode(), addr)


threading.Thread(target=receiver, daemon=True).start()

while True:
    time.sleep(1)