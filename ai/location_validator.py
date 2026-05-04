from database.db_locations import locations
from rapidfuzz import process, fuzz


class LocationValidator:
    def __init__(self, match_threshold=80):
        self.threshold = match_threshold

        # Load all barangays and streets from db_locations.py
        self.barangays = []
        self.streets = []
        self.location_rows = []

        self._load_locations()

    def _load_locations(self):
        for id, barangay, street, latitude, longitude in locations:
            self.location_rows.append(
                {
                    "id": id,
                    "barangay": barangay.lower() if barangay else None,
                    "street": street.lower() if street else None,
                    "latitude": latitude,
                    "longitude": longitude,
                }
            )

            if barangay:
                self.barangays.append(barangay.lower())

            if street:
                self.streets.append(street.lower())

    def get_row_from_matches(self, barangay_match, street_match):
        # 1. PERFECT MATCH (Both found)
        if barangay_match and street_match:
            for row in self.location_rows:
                if row["barangay"] == barangay_match and row["street"] == street_match:
                    return row

        # 2. STREET ONLY (Check if this street is unique to ONE barangay)
        if street_match and not barangay_match:
            possible_rows = [
                r for r in self.location_rows if r["street"] == street_match
            ]
            if len(possible_rows) == 1:
                return possible_rows[0]  # Found the only place this street exists!

        # 3. BARANGAY ONLY (Return the general barangay area)
        if barangay_match:
            # Try to find a row that represents the barangay broadly (often where street is None)
            for row in self.location_rows:
                if row["barangay"] == barangay_match and (
                    row["street"] is None or row["street"] == ""
                ):
                    return row

        # 4. FALLBACK
        return {
            "id": None,
            "barangay": barangay_match or "",
            "street": street_match or "",
            "latitude": None,
            "longitude": None,
        }

    def best_match_substring(self, post_text, location_list, ngram_range=(1, 3)):
        tokens = post_text.lower().split()
        best_match = None
        best_score = 0

        # Generate and check n-grams in one pass
        for n in range(ngram_range[0], ngram_range[1] + 1):
            for i in range(len(tokens) - n + 1):
                ngram = " ".join(tokens[i : i + n])
                match, score = process.extractOne(
                    ngram, location_list, scorer=fuzz.token_sort_ratio
                )[:2]

                if score > best_score:
                    best_score = score
                    best_match = match

        if best_score >= self.threshold:
            return best_match, best_score
        return None, None

    def matchBarangay(self, post_text):
        match, score = self.best_match_substring(post_text, self.barangays)
        # print(f"[Barangay - Match: {match} | Score: {score}]")
        return match

    def matchStreet(self, post_text):
        match, score = self.best_match_substring(post_text, self.streets)
        # print(f"[Street - Match: {match} | Score: {score}]")
        return match
