import sqlite3
import re

def normalize_tag_for_prompt(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s\-_]", "", s)  # letters, digits, space, hyphen, underscore
    s = re.sub(r"\s+", " ", s).strip()
    return s

def parse_instinct_txt(txt_path: str, trait_profile_id: str):
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    rules = []

    # Track current OCEAN trait, caution, curiosity, and empathy
    current_trait = None
    ca = None     # Caution HIGH / MEDIUM / LOW
    cu_band = None   # Curiosity Low / Mid / High
    em_band = None     # Empathy Low / Mid / High

    ca_map = {
        "HIGH CAUTION": (61, 100),
        "MEDIUM CAUTION": (21, 60),
        "LOW CAUTION": (1, 20),
    }

    cu_map = {
        "Low Curiosity": (1, 20),
        "Mid Curiosity": (21, 60),
        "High Curiosity": (61, 100),
    }

    em_map = {
        "Low Empathy": (1, 33),
        "Mid Empathy": (34, 66),
        "High Empathy": (67, 100),
    }

    for line in lines:
        # OCEAN trait header
        if line.startswith("["):
            content = line[1:-1].strip()
            if content in ["Neuroticism", "Agreeableness", "Extraversion", "Conscientiousness", "Openness"] and trait_profile_id.endswith(content):
                current_trait = content
                caution = None
                cu_band = None
                em_band = None
                
            elif content in ["HIGH CAUTION", "MEDIUM CAUTION", "LOW CAUTION"]:
                ca = content
                cu_band = None
                em_band = None
            elif content in ["Low Curiosity", "Mid Curiosity", "High Curiosity"]:
                cu_band = content
                em_band = None

        if " = " in line and "[" in line and "]" in line:
            # Extract tag name and value
            parts = line.split(" = ", 1)
            key_part = parts[0].strip()
            raw_text = parts[1].strip()

            if key_part.startswith("[") and key_part.endswith("]"):
                key = key_part[1:-1].strip()

                if key in ["Low Empathy", "Mid Empathy", "High Empathy"]:
                    em_band = key

                    if ca and cu_band and em_band:
                        c_low, c_high = ca_map[ca]
                        u_low, u_high = cu_map[cu_band]
                        e_low, e_high = em_map[em_band]

                        tag = normalize_tag_for_prompt(raw_text)

                        rule = {
                            "profile_id": trait_profile_id,
                            "caution": (c_low, c_high),
                            "curiosity": (u_low, u_high),
                            "empathy": (e_low, e_high),
                            "value": tag,
                        }
                        rules.append(rule)

    return rules

def expand_rules_to_rows(rules):
    rows = []

    for rule in rules:
        pc_low, pc_high = rule["caution"]
        pu_low, pu_high = rule["curiosity"]
        pe_low, pe_high = rule["empathy"]
        value = rule["value"]
        profile_id = rule["profile_id"]

        for c in range(pc_low, pc_high + 1):
            for u in range(pu_low, pu_high + 1):
                for e in range(pe_low, pe_high + 1):
                    rows.append({
                        "profile_id": profile_id,
                        "caution": c,
                        "curiosity": u,
                        "empathy": e,
                        "value": value,
                    })

    return rows

def write_to_sqlite(rows, db_path="aci_memory.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print([(r["profile_id"], r["caution"], r["curiosity"], r["empathy"], r["value"]) for r in rows[:5]])  # Print first 5 rows for verification

    # Insert or ignore duplicates by (profile_id, caution, curiosity, empathy)
    cur.executemany(
        """
        INSERT OR IGNORE INTO personality_tags
            (profile_id, caution, curiosity, empathy, value)
            VALUES (?, ?, ?, ?, ?)
        """,
        [
            (r["profile_id"], r["caution"], r["curiosity"], r["empathy"], r["value"])
            for r in rows
        ],
    )

    conn.commit()
    conn.close()

def ensure_personality_table(db_path="aci_memory.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS personality_tags (
            profile_id TEXT NOT NULL,
            caution INTEGER NOT NULL,
            curiosity INTEGER NOT NULL,
            empathy INTEGER NOT NULL,
            value TEXT NOT NULL,
            UNIQUE (profile_id, caution, curiosity, empathy)
        )
    """)
    conn.commit()
    conn.close()

def create_aci_db(mbti="ENFP", trait_letter="N", db_path="aci_memory.db"):
    ensure_personality_table(db_path)
    txt_path = "instinct_txts/{mbti}-Tag-Library.txt".format(mbti=mbti)
    trait = {
        "O": "Openness",
        "C": "Conscientiousness",
        "E": "Extraversion",
        "A": "Agreeableness",
        "N": "Neuroticism"
    }[trait_letter]
    profile_id = f"{mbti}_{trait}"

    rules = parse_instinct_txt(txt_path, profile_id)
    rows = expand_rules_to_rows(rules)
    write_to_sqlite(rows)

    print(f"Success! {len(rules)} rule cells → {len(rows)} instinct tag rows inserted for {profile_id}.")