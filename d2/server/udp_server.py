import socket
import time
from state import update_state
from database import insert_event
from config import HOST, PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print("UDP monitoring server running on", PORT)

packet_count = 0
start_time = time.time()
latency_samples = []


while True:

    data, addr = sock.recvfrom(4096)

    recv_time = time.time()

    packet_count += 1

    try:
        msg = data.decode()

        node, seq, ts, event, metric, value = msg.split("|")

        ts = int(ts)

        # latency calculation
        latency = recv_time - ts
        latency_samples.append(latency)

        update_state(node, addr[0], ts, event, metric, value)

        insert_event(node, event, metric, value, ts)

    except Exception as e:
        print("Invalid packet:", e)

    elapsed = time.time() - start_time

    if elapsed >= 10:

        throughput = packet_count / elapsed

        avg_latency = 0
        if latency_samples:
            avg_latency = sum(latency_samples) / len(latency_samples)

        print("\n========== PERFORMANCE ==========")
        print("Throughput:", round(throughput, 2), "packets/sec")
        print("Average latency:", round(avg_latency, 4), "sec")
        print("Packets processed:", packet_count)
        print("=================================\n")

        start_time = time.time()
        packet_count = 0
        latency_samples = []