import ollama
from typing import Tuple, List
from database.db_keywords import keyword_dict  # Pulling your existing dict


class OllamaNLP:
    def __init__(self, model_name: str = "ministral-3:14b-cloud") -> None:
        self.model_name: str = model_name
        # Dynamically grab the categories straight from your database file!
        self.valid_categories: List[str] = list(keyword_dict.keys())

    def extract_intent(self, post_text: str) -> Tuple[str, float]:
        """
        Sends the text to Ollama's cloud model for classification.
        Returns a tuple of (category_name, confidence_score).
        """

        prompt: str = f"""
        You are a highly precise classification AI. You understand English, Tagalog, and Bisaya natively.
        
        Classify the following user message into exactly ONE of these categories:
        {', '.join(self.valid_categories)}, or Unknown.

        Rules:
        1. Respond ONLY with the exact category name.
        2. If the text does not match any category, or if it is gibberish/keyboard smash, respond with Unknown.
        3. Do not add punctuation, conversational text, or explanations.

        Message: "{post_text}"
        """

        try:
            # Routes the prompt directly to Ollama's cloud servers
            response: any = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            # Extract and clean the LLM's response
            intent: str = response["message"]["content"].strip()
            # Strip extra punctuation just in case the LLM tries to be conversational
            intent = "".join(c for c in intent if c.isalnum() or c == "_")

            if intent in self.valid_categories:
                return intent, 1.0
            else:
                return "Unknown", 0.0

        except Exception as e:
            print(f"[Ollama Cloud Error] {e}")
            return "Unknown", 0.0
