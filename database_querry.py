import sqlite3

DB_PATH = "aci_memory.db"

def run_query(query=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if query is None:
        while True:
            query = input("\nSQL> ").strip()
    else:
        cur.execute(query)


        try:
            cur.execute(query)

            if query.lower().startswith("select"):
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No results.")
            else:
                conn.commit()
                print("Query executed successfully.")

        except Exception as e:
            print(f"Error: {e}")

    conn.close()

if __name__ == "__main__":
    run_query('''SELECT 
    e.event_id,
    e.time_of_event,
    e.created_at,
    env.env_name,
    et.tag,
    ee.emotion
    FROM events e
    JOIN environments env ON e.env_id = env.env_id
    LEFT JOIN event_tags et ON e.event_id = et.event_id
    LEFT JOIN event_emotions ee ON e.event_id = ee.event_id
    WHERE e.created_at BETWEEN '2026-03-01 00:00:00' AND '2026-04-05 23:59:59'
    ORDER BY e.created_at ASC;''')