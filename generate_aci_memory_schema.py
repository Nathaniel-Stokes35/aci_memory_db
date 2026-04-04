from datetime import datetime, timedelta
import sqlite3

def create_aci_db(db_path="aci_memory.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Drop tables first so can be run multiple times
    cur.executescript("""
        DROP TABLE IF EXISTS event_emotions;
        DROP TABLE IF EXISTS event_tags;
        DROP TABLE IF EXISTS event_people;
        DROP TABLE IF EXISTS events;
        DROP TABLE IF EXISTS environments;
        DROP TABLE IF EXISTS personality_tags;
    """)

    # Environments: kitchen, living_room, school, etc.
    cur.execute("""
        CREATE TABLE environments (
            env_id INTEGER PRIMARY KEY AUTOINCREMENT,
            env_name TEXT NOT NULL UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Events: each ACI‑relevant interaction / evaluation
    cur.execute("""
        CREATE TABLE events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            env_id INTEGER NOT NULL,
            time_of_event TEXT NOT NULL,
            raw_text TEXT NOT NULL,
            danger_score REAL DEFAULT 0.0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(env_id) REFERENCES environments(env_id)
        )
    """)

    # People involved in the event
    cur.execute("""
        CREATE TABLE event_people (
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            person_name TEXT NOT NULL,
            role TEXT NOT NULL,  -- e.g., user, observer, caregiver
            FOREIGN KEY(event_id) REFERENCES events(event_id)
        )
    """)

    # General tags for the event
    cur.execute("""
        CREATE TABLE event_tags (
            tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            tag TEXT NOT NULL,
            weight REAL DEFAULT 1.0,
            FOREIGN KEY(event_id) REFERENCES events(event_id)
        )
    """)

    # Emotional tags for the event
    cur.execute("""
        CREATE TABLE event_emotions (
            emotion_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            emotion TEXT NOT NULL,
            intensity REAL NOT NULL DEFAULT 0.5,
            FOREIGN KEY(event_id) REFERENCES events(event_id)
        )
    """)

    # Personality tags for the event (e.g., "ENFP_N" for Neuroticism score of an ENFP)
    cur.execute("""
            CREATE TABLE personality_tags (
                profile_id TEXT NOT NULL,
                caution INTEGER NOT NULL,
                curiosity INTEGER NOT NULL,
                empathy INTEGER NOT NULL,
                value TEXT NOT NULL,
                UNIQUE (profile_id, caution, curiosity, empathy)
        );
    """)

    print("ACI event memory schema created at: aci_memory.db")
    print("Generating Artifical Events to populate Tables for filtering and production testing...")

    populate_sample_data(db_path)

    conn.commit()
    conn.close()

def populate_sample_data(db_path="aci_memory.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # --- Environments ---
    cur.executemany(
        "INSERT INTO environments (env_name) VALUES (?)",
        [("kitchen",), ("living_room",), ("school",)]
    )

    # --- Events ---
    now = datetime.now()
    events = [
        (1, now - timedelta(days=3), "Saw a cat in the kitchen", 0.1),
        (2, now - timedelta(days=2), "Studied in living room", 0.0),
        (3, now - timedelta(days=1), "Talked to a friend at school", 0.2)
    ]
    cur.executemany(
        "INSERT INTO events (env_id, time_of_event, raw_text, danger_score) VALUES (?, ?, ?, ?)",
        [(e[0], e[1].isoformat(), e[2], e[3]) for e in events]
    )

    # --- Event Tags ---
    cur.executemany(
        "INSERT INTO event_tags (event_id, tag, weight) VALUES (?, ?, ?)",
        [(1, "cat", 1.0), (2, "study", 0.8), (3, "friend", 0.9)]
    )

    # --- Event Emotions ---
    cur.executemany(
        "INSERT INTO event_emotions (event_id, emotion, intensity) VALUES (?, ?, ?)",
        [(1, "surprised", 0.6), (2, "focused", 0.7), (3, "happy", 0.8)]
    )

    personalities = [
        ("ENFP_N", 30, 90, 80, "Curious Dreamer"),
        ("ISTJ_O", 80, 40, 60, "Practical Analyst"),
        ("INTP_N", 25, 95, 30, "Inventive Theorist")
    ]

    cur.executemany(
        "INSERT INTO personality_tags (profile_id, caution, curiosity, empathy, value) VALUES (?, ?, ?, ?, ?)",
        personalities
    )

    conn.commit()
    conn.close()
    print("Sample data populated in ACI memory database at: aci_memory.db")

if __name__ == "__main__":
    create_aci_db()