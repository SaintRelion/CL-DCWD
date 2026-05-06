from database.db_locations import location_dict
from rapidfuzz import process, fuzz
from typing import Optional, Dict, Any, Tuple


class LocationValidator:
    def __init__(self, match_threshold: int = 80):
        self.threshold: int = match_threshold

        self.barangays: list[str] = []
        self.location_rows: list[Dict[str, Any]] = []

        self._load_locations()

    def _load_locations(self) -> None:
        # Pull directly from our cleaned-up location_dict mapping
        for loc_id, loc_data in location_dict.items():
            barangay: str = loc_data["barangay"]

            self.location_rows.append(
                {
                    "id": loc_id,
                    "barangay": barangay.lower(),
                    "latitude": loc_data["latitude"],
                    "longitude": loc_data["longitude"],
                }
            )

            if barangay:
                self.barangays.append(barangay.lower())

    def get_row_from_matches(self, barangay_match: Optional[str]) -> Dict[str, Any]:
        """
        Takes a matched barangay string and returns the full location dictionary row.
        """
        if barangay_match:
            for row in self.location_rows:
                if row["barangay"] == barangay_match:
                    return row

        # FALLBACK
        return {
            "id": None,
            "barangay": barangay_match or "",
            "latitude": None,
            "longitude": None,
        }

    def best_match_substring(
        self,
        post_text: str,
        location_list: list[str],
        ngram_range: Tuple[int, int] = (1, 3),
    ) -> Optional[str]:
        tokens: list[str] = post_text.lower().split()
        best_match: Optional[str] = None
        best_score: int = 0

        # Generate and check n-grams in one pass
        for n in range(ngram_range[0], ngram_range[1] + 1):
            for i in range(len(tokens) - n + 1):
                ngram: str = " ".join(tokens[i : i + n])
                match, score = process.extractOne(
                    ngram, location_list, scorer=fuzz.token_sort_ratio
                )[:2]

                if score > best_score:
                    best_score = score
                    best_match = match

        if best_score >= self.threshold:
            return best_match

        return None

    def matchBarangay(self, post_text: str) -> Optional[str]:
        match = self.best_match_substring(post_text, self.barangays)
        return match
