from generate_aci_memory_schema import create_aci_db
from parse_instinct_tag_library import create_aci_db as insert_aci_data

def create_aci(mbti: str, ocean: str):
    # Convert trait letter to full name
    trait_letter_map = {
        "O": "Openness",
        "C": "Conscientiousness",
        "E": "Extraversion",
        "A": "Agreeableness",
        "N": "Neuroticism"
    }
    trait_full = trait_letter_map.get(ocean.upper())
    create_aci_db()  # ensures tables exist
    insert_aci_data(mbti, ocean)  # insert/update new MBTI + trait
    print(f"ACI created/updated for {mbti}: {trait_full}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python create_aci.py <MBTI> <TraitLetter>")
        sys.exit(1)

    mbti = sys.argv[1]
    ocean = sys.argv[2]

    create_aci(mbti, ocean)