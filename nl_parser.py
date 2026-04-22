import re
from typing import Any



def parse_natural_query(q: str) -> dict[str, Any] | None:
    q = q.lower().strip()
    filters = {}

    # Gender Handling
    has_male = bool(re.search(r'\bmale(s)?\b', q))
    has_female = bool(re.search(r'\bfemale(s)?\b', q))

    if has_male and has_female:
        # "male and female"
        pass
    elif has_male:
        filters["gender"] = "male"
    elif has_female:
        filters["gender"] = "female"

    # Check for age related
    if re.search(r'\b(teenager(s)?|teen|teens)\b', q):
        filters["age_group"] = "teenager"
        if "above 17" in q or "over 17" in q:
            filters["min_age"] = 17

    if re.search(r'\byoung\b', q):
        filters["min_age"] = 16
        filters["max_age"] = 24

    if re.search(r'\badult\b', q):
        filters["age_group"] = "adult"

    # Age ranges
    above_match = re.search(r'(above|over|older than)\s+(\d+)', q)
    if above_match:
        filters["min_age"] = int(above_match.group(2))

    below_match = re.search(r'(below|under|younger than)\s+(\d+)', q)
    if below_match:
        filters["max_age"] = int(below_match.group(2))

    # Country
    country_map = {
        "nigeria": "NG",
        "kenya": "KE",
        "angola": "AO",
        "central african republic": "CF",
        "tanzania": "TZ",
        "uganda": "UG"
    }

    for word, code in country_map.items():
        if word in q:
            filters["country_id"] = code
            break

    # "males and females" → remove gender filter
    #if "male and female" in q or "males and females" in q:
        #filters.pop("gender", None)

    return filters if filters else None