from database.db_base import db_cursor, conn
from typing import List, Tuple, Dict

# Fetch only the id and category
db_cursor.execute("SELECT id, category FROM keywords;")
keywords_data: List[Tuple[int, str]] = db_cursor.fetchall()

# Clean 1:1 mapping: "category_name" -> id
keyword_dict: Dict[str, int] = {
    category.lower(): kw_id for kw_id, category in keywords_data
}
