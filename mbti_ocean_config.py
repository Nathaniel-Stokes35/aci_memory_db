# mbti_ocean_config.py

# 16 MBTI types
MBTI_TYPES = [
    "ESTJ", "ESTP", "ESFJ", "ESFP",
    "ENTJ", "ENTP", "ENFJ", "ENFP",
    "ISTJ", "ISTP", "ISFJ", "ISFP",
    "INTJ", "INTP", "INFJ", "INFP"
]

# 5 OCEAN traits
OCEAN_TRAITS = ["O", "C", "E", "A", "N"]  # Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism

def get_profile_id(mbt, trait_letter):
    return f"{mbt}_{trait_letter}"

# Example: "ENFP_N" → read from "ENFP.txt [Neuroticism]"