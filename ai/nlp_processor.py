import re

from rapidfuzz import process, fuzz
from sentence_transformers import SentenceTransformer, util

from database.db_keywords import keyword_dict

# ── domain anchors ────────────────────────────────────────────────────────────
# Broad "is this even about water?" check before classifying.
# Not categories — just water-related concepts in all three languages.
DOMAIN_ANCHORS = [
    "water",
    "tubig",
    "gripo",
    "tubo",
    "baha",
    "hugaw",
    "tulo",
    "basa",
    "drainage",
    "suplay",
    "water supply",
    "patay ang tubig",
    "water problem",
    "linya",
    "kanal",
    "estero",
    "gripo",
    "poso",
]


class NLPProcessor:
    def __init__(self, threshold=0.55, domain_threshold=0.35, fuzzy_threshold=85):
        self.threshold = threshold
        self.domain_threshold = domain_threshold
        self.fuzzy_threshold = fuzzy_threshold  # 0-100, how strict fuzzy match is

        self.keyword_dict = keyword_dict
        self.category_embeddings = {}

        # flat list of all keywords for fuzzy matching
        # maps keyword → category
        self.all_keywords: dict[str, str] = {}
        for cat, words in self.keyword_dict.items():
            for word in words:
                self.all_keywords[word] = cat

        print("Loading model from ./models/minilm ...")
        self.model = SentenceTransformer("./models/minilm")

        # encode keywords per category
        for cat, kws in self.keyword_dict.items():
            self.category_embeddings[cat] = self.model.encode(
                kws, convert_to_tensor=True
            )

        # encode domain anchors once
        self.anchor_embs = self.model.encode(DOMAIN_ANCHORS, convert_to_tensor=True)

    # ── normalization ─────────────────────────────────────────────────────────

    def _normalize(self, text: str) -> str:
        """
        hugawwww  → hugaw   (collapse 3+ repeated chars)
        huga w    → huga w  (leave real short words alone)
        """
        return re.sub(r"(.)\1{2,}", r"\1", text)

    # ── gibberish check ───────────────────────────────────────────────────────

    def _is_gibberish(self, text: str) -> bool:
        normalized = self._normalize(text)
        words = normalized.split()

        # long word with no vowels → keyboard smash
        for word in words:
            if len(word) > 10 and not any(v in word for v in "aeiouy"):
                return True

        # single long string with no spaces → gibberish
        if len(text) > 20 and " " not in text:
            return True

        return False

    # ── domain check ──────────────────────────────────────────────────────────

    def _is_in_domain(self, text: str) -> tuple[bool, float]:
        emb = self.model.encode(text, convert_to_tensor=True)
        sims = util.cos_sim(emb, self.anchor_embs)
        best = sims.max().item()
        return best >= self.domain_threshold, best

    # ── fuzzy literal match ───────────────────────────────────────────────────

    def _get_fuzzy_threshold(self, word: str) -> int:
        """
        Short words need a stricter threshold to avoid false matches.
          len ≤ 4  → 100 (exact only) — "tulo" hits "tulo", "valo" hits nothing
          len ≤ 6  → 90  (one typo)   — "hugaw" → "hugaw", "hugw" → "hugaw"
          len 7+   → 85  (normal)     — longer words, more lenient
        """
        length = len(word)
        if length <= 4:
            return 100
        if length <= 6:
            return 90
        return 85

    def _fuzzy_literal_match(self, text: str) -> tuple[bool, str, str]:
        """
        Check each word in the text against SINGLE-WORD keywords only.
        Multi-word keywords like "hugaw ang tubig" are skipped —
        MiniLM handles those via semantic similarity.

        Uses dynamic threshold per word length so short words like
        "tulo" only match exactly, while longer words allow typos.

        This handles:
          tulo   → tulo   (exact, len=4, threshold=100) ✓
          valo   → no match (len=4, threshold=100, not a water word) ✓
          hugw   → hugaw  (len=4 after norm, threshold=100... close enough)
          hugaw  → hugaw  (len=5, threshold=90) ✓
          malabo → malabo (len=6, threshold=90) ✓
        """
        words = text.split()

        # only fuzzy against single-word keywords — phrases are MiniLM's job
        single_kws = {kw: cat for kw, cat in self.all_keywords.items() if " " not in kw}
        single_kw_list = list(single_kws.keys())

        for word in words:
            if len(word) < 3:  # skip pure particles: sa, ng, ay
                continue

            threshold = self._get_fuzzy_threshold(word)
            result = process.extractOne(
                word,
                single_kw_list,
                scorer=fuzz.ratio,
                score_cutoff=threshold,
            )
            if result:
                matched_kw, score, _ = result
                category = single_kws[matched_kw]
                return True, matched_kw, category

        return False, "", ""

    # ── main intent extraction ────────────────────────────────────────────────

    def extract_intent(self, post_text: str) -> tuple[str, float]:
        # Step 1 — normalize elongated words
        normalized = self._normalize(post_text)
        normalized_lower = normalized.lower()

        # Step 2 — gibberish filter
        if self._is_gibberish(normalized_lower):
            return "Unknown", 0.0

        # Step 3 — domain filter (is this even about water?)
        in_domain, domain_score = self._is_in_domain(normalized)
        if not in_domain:
            return "Unknown", 0.0

        # Step 4 — fuzzy literal match (handles typos + shortcuts)
        # If a word in the sentence fuzzy-matches a keyword, we trust it strongly
        fuzzy_hit, matched_kw, fuzzy_cat = self._fuzzy_literal_match(normalized_lower)

        # Step 5 — semantic similarity across all categories
        results = {}
        post_emb = self.model.encode(normalized, convert_to_tensor=True)

        for cat, kw_embs in self.category_embeddings.items():
            sims = util.cos_sim(post_emb, kw_embs)
            max_sim = sims.max().item()

            # fuzzy boost: if the fuzzy match pointed to this category, boost it
            if fuzzy_hit and fuzzy_cat == cat:
                final_score = max(max_sim, 0.92)
            else:
                final_score = max_sim

            results[cat] = final_score

        best_cat = max(results, key=results.get)
        confidence = results[best_cat]

        if confidence < self.threshold:
            return "Unknown", confidence

        return best_cat, confidence
