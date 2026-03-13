import socket
import threading
import time
from collections import defaultdict
from cryptography.fernet import Fernet

HOST = "0.0.0.0"
PORT = 9000

KEY = b'4N0zPj3C9j2mA2y7eFzQ4jYx6yXr0cZy4Yp9sL9Q6V0='
cipher = Fernet(KEY)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print("Secure Monitoring Server running on port", PORT)

nodes = {}
event_counts = defaultdict(int)
last_seq = {}

lock = threading.Lock()


def receiver():

    while True:

        data, addr = sock.recvfrom(4096)

        try:
            decrypted = cipher.decrypt(data).decode()

            node, seq, ts, event, metric, value = decrypted.split("|")

            seq = int(seq)
            ts = int(ts)

        except:
            print("Invalid packet received")
            continue

        with lock:

            if node not in nodes:
                nodes[node] = {}

            if node in last_seq and seq != last_seq[node] + 1:
                print("Packet loss suspected from", node)

            last_seq[node] = seq

            nodes[node]["ip"] = addr[0]
            nodes[node]["last_seen"] = ts
            nodes[node]["event"] = (event, metric, value)

            event_counts[event] += 1


def dashboard():

    while True:

        time.sleep(3)

        with lock:

            print("\n========= NETWORK DASHBOARD =========")

            now = int(time.time())

            print("\nActive Nodes")

            for node in nodes:

                age = now - nodes[node]["last_seen"]

                status = "ONLINE"
                if age > 10:
                    status = "OFFLINE"

                print(
                    f"{node} | {nodes[node]['ip']} | {status} | {age}s ago"
                )

            print("\nLatest Events")

            for node in nodes:

                event, metric, value = nodes[node]["event"]

                print(f"{node} -> {event} ({metric}={value})")

            print("\nEvent Counts")

            for e in event_counts:
                print(e, ":", event_counts[e])

            print("=====================================")


threading.Thread(target=receiver, daemon=True).start()

dashboard()