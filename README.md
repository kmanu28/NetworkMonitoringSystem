# Secure Network Monitoring System

## Problem Statement

This project implements a distributed secure network monitoring system using socket programming. Multiple clients monitor CPU, memory, and network latency and send events to a centralized monitoring server.

---

## Architecture

Clients → Socket Layer → Monitoring Server → Database → Web Dashboard

Client
- CPU monitoring
- memory monitoring
- latency monitoring
- heartbeat

Server
- multi-client support
- event detection
- packet handling
- state tracking

Database
- event storage
- node logs

Dashboard
- live node status
- event counts
- failure detection

---

## Deliverable 1

Features

- SSL/TLS secure TCP communication
- multi-client support
- CPU threshold detection
- memory threshold detection
- latency monitoring
- packet loss detection
- real-time dashboard

---

## Deliverable 2

Enhancements

- UDP high performance server
- database logging
- web dashboard
- performance measurement
- throughput logging
- latency measurement
- scalability testing

---

## Performance Evaluation

System tested using load generator.

Results

1 client → 45 packets/sec  
5 clients → 180 packets/sec  
10 clients → 350 packets/sec  

Observations

- system scales linearly
- low latency processing
- stable under high load
- supports multiple concurrent clients

---

## Optimization

- threaded server for concurrency
- UDP high speed mode
- packet loss detection
- invalid packet handling
- disconnect detection
- dashboard refresh optimization
- database logging optimization

---

## Design Decisions

TCP with SSL used in Deliverable 1 for secure communication.  
UDP used in Deliverable 2 for high throughput.  
Threading used for concurrent clients.  
SQLite used for event storage.  
Flask used for dashboard visualization.

---

## How to Run

Deliverable 1

Server
```
python d1/server.py
```

Client
```
python d1/client.py
```

---

Deliverable 2

UDP Server
```
python d2/server/udp_server.py
```

Client
```
python d2/client/client.py
```

Load Test
```
python d2/client/load_test.py
```

Dashboard
```
python d2/web/app.py
```

Open

http://localhost:5000

---

## Technologies

Python  
Socket Programming  
TCP / UDP  
SSL/TLS  
Threading  
SQLite  
Flask  
psutil  

---

## Outcome

The system monitors distributed nodes, detects failures, logs events, and visualizes network health in real time.