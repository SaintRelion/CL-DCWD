import json
import time
import requests
from typing import List, Dict
from database.db_keywords import keyword_dict

CHUTES_API_URL = "https://llm.chutes.ai/v1/chat/completions"


class ChutesNLP:
    def __init__(
        self,
        model_name: str = "google/gemma-4-31B-turbo-TEE",
        max_retries: int = 5,
        retry_delay: float = 5.0,
    ) -> None:
        self.model_name: str = model_name
        self.max_retries: int = max_retries
        self.retry_delay: float = retry_delay
        # Pull category keys dynamically from our unified keyword dictionary
        self.valid_categories: List[str] = list(keyword_dict.keys())

        self.api_key: str = (
            "cpk_3c2497bb059b4fc4ab320aca6b039950.4075e624b7585b3f99ebfb8c03fd03aa.lUgrmeemCo0TdAeRuiWCjVXEBxfBdiuJ"
        )

        self.headers: Dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def extract_intent(self, post_text: str) -> str:
        """
        Classifies a single post.
        Returns the category string (e.g., 'leak', 'no_water', or 'Unknown').
        """
        results = self._batch_classify([post_text])
        return results[0]["intent"]

    def batch_extract_intent(self, posts: List[str]) -> List[Dict[str, str]]:
        """
        Classifies a list of posts in a SINGLE API request.
        Returns a list of dicts: [{"post": "...", "intent": "leak"}, ...]
        """
        return self._batch_classify(posts)

    def _build_prompt(self, posts: List[str]) -> str:
        categories_str = ", ".join(self.valid_categories)
        numbered = "\n".join(f"{i+1}. {p}" for i, p in enumerate(posts))

        return f"""You are a precise classification AI. You understand English, Tagalog, and Bisaya/Cebuano natively.

Classify each post into exactly ONE of these categories: {categories_str}, or Unknown.

Rules:
1. Respond ONLY with a JSON array of category names, one per post, in the same order.
2. Use Unknown if the post does not match any category, is gibberish, keyboard smash, or unrelated to water incidents.
3. Do not add explanations, punctuation, or markdown. Just the raw JSON array.

Example response format: ["dirty water", "leak", "Unknown", "no water"]

Posts:
{numbered}"""

    def _batch_classify(self, posts: List[str]) -> List[Dict[str, str]]:
        prompt = self._build_prompt(posts)

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 200,
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(
                    CHUTES_API_URL,
                    headers=self.headers,
                    json=payload,
                    timeout=30,
                )

                if response.status_code == 429:
                    wait = self.retry_delay * attempt
                    print(
                        f"[Chutes] Rate limited. Waiting {wait}s (attempt {attempt}/{self.max_retries})"
                    )
                    time.sleep(wait)
                    continue

                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"].strip()
                labels = self._parse_labels(content, len(posts))
                return self._build_results(posts, labels)

            except requests.exceptions.Timeout:
                print(f"[Chutes] Timeout on attempt {attempt}/{self.max_retries}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

            except Exception as e:
                print(f"[Chutes Error] {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)

        print("[Chutes] All retries failed. Returning Unknown for all posts.")
        return self._build_results(posts, ["Unknown"] * len(posts))

    def _parse_labels(self, content: str, expected_count: int) -> List[str]:
        try:
            clean = content.replace("```json", "").replace("```", "").strip()
            labels = json.loads(clean)

            if not isinstance(labels, list):
                raise ValueError("Response is not a list")

            result = []
            for label in labels[:expected_count]:
                # Allow spaces, letters, numbers, and underscores
                normalized = (
                    "".join(
                        c for c in str(label) if c.isalnum() or c == "_" or c == " "
                    )
                    .strip()
                    .lower()
                )

                # Check against valid_categories using relaxed matching
                matched_category = "Unknown"
                for valid_cat in self.valid_categories:
                    if (
                        valid_cat.replace(" ", "").lower()
                        == normalized.replace(" ", "").lower()
                    ):
                        matched_category = valid_cat
                        break

                result.append(matched_category)

            while len(result) < expected_count:
                result.append("Unknown")

            return result

        except (json.JSONDecodeError, ValueError) as e:
            print(f"[Chutes] Failed to parse response: {content!r} — {e}")
            return ["Unknown"] * expected_count

    def _build_results(
        self, posts: List[str], labels: List[str]
    ) -> List[Dict[str, str]]:
        return [{"post": post, "intent": label} for post, label in zip(posts, labels)]
