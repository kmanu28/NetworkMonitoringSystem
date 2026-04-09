import socket
import time
import random

SERVER_IP = "127.0.0.1"
PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Load test started")

while True:

    node = "loadtest"

    seq = random.randint(1,100000)

    ts = int(time.time())

    msg = f"{node}|{seq}|{ts}|HEARTBEAT|cpu|20"

    sock.sendto(msg.encode(), (SERVER_IP, PORT))

    time.sleep(0.005)