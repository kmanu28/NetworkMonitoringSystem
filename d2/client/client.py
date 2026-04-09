import socket
import time
import psutil
from ping3 import ping
from cryptography.fernet import Fernet
import uuid

SERVER_IP = "127.0.0.1"
PORT = 9000

NODE_ID = f"node-{uuid.uuid4().hex[:6]}"

KEY = b'4N0zPj3C9j2mA2y7eFzQ4jYx6yXr0cZy4Yp9sL9Q6V0='
cipher = Fernet(KEY)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq = 0

COOLDOWN = 10
last_sent = {}


def should_send(event):
    now = time.time()
    if event not in last_sent or now - last_sent[event] > COOLDOWN:
        last_sent[event] = now
        return True
    return False


def send_event(event, metric, value):
    global seq
    seq += 1

    ts = int(time.time())
    msg = f"{NODE_ID}|{seq}|{ts}|{event}|{metric}|{value}"

    encrypted = cipher.encrypt(msg.encode())
    sock.sendto(encrypted, (SERVER_IP, PORT))

    print("Sending:", msg)


def heartbeat():
    send_event("HEARTBEAT", "status", "alive")


def check_cpu():
    cpu = psutil.cpu_percent(interval=1)
    if cpu > 2 and should_send("CPU_THRESHOLD_EXCEEDED"):
        send_event("CPU_THRESHOLD_EXCEEDED", "cpu", cpu)


def check_memory():
    mem = psutil.virtual_memory().percent
    if mem > 10 and should_send("MEMORY_THRESHOLD_EXCEEDED"):
        send_event("MEMORY_THRESHOLD_EXCEEDED", "memory", mem)


def check_latency():
    try:
        latency = ping("8.8.8.8", timeout=1)
    except Exception as e:
        print("Ping error:", e)
        return

    if latency is None:
        send_event("NETWORK_FAILURE", "latency", 0)
    elif latency > 0.01 and should_send("LATENCY_HIGH"):
        send_event("LATENCY_HIGH", "latency", latency)


print("Client started:", NODE_ID)

try:
    while True:
        heartbeat()
        check_cpu()
        check_memory()
        check_latency()
        time.sleep(3)
except Exception as e:
    print("ERROR:", e)
    input("Press Enter to exit...")