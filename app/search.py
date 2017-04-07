from .db import get_db, close_connection


def search(query, paper, author):
    db = get_db()
    cursor = db.cursor()
    return cursor
