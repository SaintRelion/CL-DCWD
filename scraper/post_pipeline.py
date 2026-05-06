from datetime import datetime
from typing import List, Tuple, Dict, Any

from ai.location_validator import LocationValidator
from ai.chutes_nlp import ChutesNLP
from database.db_posts import insert_post

nlp = ChutesNLP()
lv = LocationValidator()


def process_post(raw_posts: List[Dict[str, str]], scraper_init: datetime) -> None:
    """
    Expects raw_posts to be a list of tuples: [(post_text, username, profile_link), ...]
    """
    if not raw_posts:
        return

    # Extract just the text for the NLP batch call
    post_texts: List[str] = [item["text"] for item in raw_posts]

    # One API call for the whole scroll, returns List[Dict[str, str]] -> {"post": "...", "intent": "..."}
    results = nlp.batch_extract_intent(post_texts)

    for i, result in enumerate(results):
        raw_text: str = result["post"]
        intent: str = result["intent"]

        # Retrieve corresponding metadata using index
        username: str = raw_posts[i]["name"]
        profile_link: str = raw_posts[i]["link"]

        barangay: str = lv.matchBarangay(raw_text)
        location_row: Dict[str, Any] = lv.get_row_from_matches(barangay)

        # Map to the strict DB-friendly UI statuses
        if intent == "Unknown":
            status = "non-incident"
        else:
            status = "under evaluation"

        # Insert updated payload (score/confidence removed)
        insert_post(
            post=raw_text,
            username=username,
            profile_link=profile_link,
            intent=intent,
            status=status,
            location_row=location_row,
            scraper_init=scraper_init,
        )
