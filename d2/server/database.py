import sqlite3

conn = sqlite3.connect("events.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS events (
    node TEXT,
    timestamp INTEGER,
    event TEXT,
    metric TEXT,
    value TEXT
)
""")
conn.commit()


def insert_event(node, ts, event, metric, value):
    cur.execute(
        "INSERT INTO events VALUES (?, ?, ?, ?, ?)",
        (node, ts, event, metric, value),
    )
    conn.commit()


def get_events():
    cur.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT 50")
    return cur.fetchall()