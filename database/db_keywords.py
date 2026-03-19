from database.db_base import db_cursor, conn

db_cursor.execute("SELECT id, word, category FROM keywords;")
keywords_data = db_cursor.fetchall()

keyword_dict = {}
for id, word, category in keywords_data:
    cat = category.lower()
    if cat not in keyword_dict:
        keyword_dict[cat] = []
    keyword_dict[cat].append(word.lower())
