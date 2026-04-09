from collections import defaultdict
import threading

nodes = {}
event_counts = defaultdict(int)
last_seq = {}

lock = threading.Lock()