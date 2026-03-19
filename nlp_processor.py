import re

from sentence_transformers import SentenceTransformer, util
from database.db_keywords import keyword_dict


class NLPProcessor:
    def __init__(self, threshold=0.55):  # Bumped threshold to 0.55
        self.threshold = threshold
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        self.keyword_dict = keyword_dict
        self.category_embeddings = {}

        for cat, kws in self.keyword_dict.items():
            self.category_embeddings[cat] = self.model.encode(
                kws, convert_to_tensor=True
            )

    def is_gibberish(self, text):
        # 1. Normalize "Emphasis" (e.g., 'hugawwww' -> 'hugaw')
        # This regex replaces 3+ repeated characters with just 1
        normalized_text = re.sub(r"(.)\1{2,}", r"\1", text)

        # 2. Check for "Keyboard Smash" (No vowels or weird consonant clusters)
        # If a long word has 0 vowels, it's likely gibberish like 'skjdfhgsdhkg'
        words = normalized_text.split()
        for word in words:
            if len(word) > 10 and not any(v in word for v in "aeiouy"):
                return True  # Keyboard smash detected

        # 3. Check for repetitive strings that aren't words (e.g., 'asdfasdfasdf')
        if len(text) > 20 and " " not in text:
            return True

        return False

    def extract_intent(self, post_text):
        text_lower = post_text.lower()

        # --- NEW: GIBBERISH PRE-FILTER ---
        if self.is_gibberish(text_lower):
            return "Unknown", 0.0

        results = {}
        post_emb = self.model.encode(post_text, convert_to_tensor=True)

        for cat, kw_embs in self.category_embeddings.items():
            sims = util.cos_sim(post_emb, kw_embs)
            max_sim = sims.max().item()

            # Literal Boost - Ensure the keyword is not just a substring of another word
            # Using regex \b matches word boundaries
            literal_match = False
            for kw in self.keyword_dict[cat]:
                if re.search(r"\b" + re.escape(kw.lower()) + r"\b", text_lower):
                    literal_match = True
                    break

            # Combine: If literal match exists, we trust it.
            # Otherwise, we use AI similarity.
            final_score = max(max_sim, 0.95 if literal_match else 0)
            results[cat] = final_score

        best_cat = max(results, key=results.get)
        confidence = results[best_cat]

        # --- HIGHER THRESHOLD ---
        if confidence < self.threshold:
            return "Unknown", confidence

        return best_cat, confidence
