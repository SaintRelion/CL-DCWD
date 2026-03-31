from nlp_processor import NLPProcessor
from location_validator import LocationValidator
from database.db_posts import insert_post

nlp = NLPProcessor()
lv = LocationValidator()


def process_post(raw_text: str):
    intent, confidence = nlp.extract_intent(raw_text)

    barangay = lv.matchBarangay(raw_text)
    street = lv.matchStreet(raw_text)
    location_row = lv.get_row_from_matches(barangay, street)

    # If NLP totally lost, it's likely a Non-Incident
    if intent == "Unknown" or confidence < 0.45:
        status = "Non-Incident"

    # If we have an intent but NO location, needs a human to find the address
    elif not location_row.get("id"):
        status = "Under Evaluation"

    # 3. If we have both, it's ready for a Tubero to click "Actual Incident"
    else:
        status = "Under Evaluation"

    insert_post(
        post=raw_text,
        intent=intent,
        score=confidence,
        status=status,
        location_row=location_row,
    )
