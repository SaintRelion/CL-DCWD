from datetime import datetime
from typing import List

from ai.location_validator import LocationValidator
from ai.chutes_nlp import ChutesNLP
from database.db_posts import insert_post

nlp = ChutesNLP()
lv = LocationValidator()


def process_post(raw_posts: List[str], scraper_init: datetime):
    if not raw_posts:
        return

    # one API call for the whole scroll
    results = nlp.batch_extract_intent(raw_posts)

    for result in results:
        raw_text = result["post"]
        intent = result["intent"]

        barangay = lv.matchBarangay(raw_text)
        street = lv.matchStreet(raw_text)
        location_row = lv.get_row_from_matches(barangay, street)

        if intent == "Unknown":
            status = "Non-Incident"
        elif not location_row.get("id"):
            status = "Under Evaluation"
        else:
            status = "Under Evaluation"

        insert_post(
            post=raw_text,
            intent=intent,
            score=1.0,  # no confidence rating, default 1
            status=status,
            location_row=location_row,
            scraper_init=scraper_init,
        )
