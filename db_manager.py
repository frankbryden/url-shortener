import sqlite3
import datetime
from typing import Optional

from constants import SLUG_LENGTH

TABLE_PREPARE = f"CREATE TABLE IF NOT EXISTS urls(url VARCHAR(2048), slug CHAR({SLUG_LENGTH}), count INT, expiry DATETIME);"
INDEX_CREATION = "CREATE UNIQUE INDEX IF NOT EXISTS idx_slugs ON urls (slug);"

class DbManager:
    def __init__(self, filename: str = "urls.db"):
        self.con = sqlite3.connect(filename,check_same_thread=False)
        self._initialize()

    def _initialize(self):
        self.con.execute(TABLE_PREPARE)
        self.con.execute(INDEX_CREATION)

    def insert_slug(self, url: str, slug: str, expiry: datetime.datetime):
        try:
            self.con.execute("INSERT INTO urls(url, slug, count, expiry) VALUES (?, ?, 0, ?)", (url, slug, expiry))
            self.con.commit()
        except sqlite3.IntegrityError:
            # Url has already been shortened - slug already in database (a, b) -> (_, b)
            # TODO ensure that the URL is the same
            pass
    
    def get_url_from_slug(self, slug) -> Optional[str]:
        resp = self.con.execute("SELECT url, count FROM urls WHERE slug=? AND (expiry IS NULL OR expiry>?)", (slug,datetime.datetime.now())).fetchall()
        # Ensure we never get more than 1 URL given a slug
        assert len(resp) < 2
        if len(resp) == 0:
            return None
        url, count = resp[0]
        print(f"{url} has been requested {count + 1} times")
        self._update_counter(slug, count + 1)
        return url

    def _update_counter(self, slug: str, count: int):
        self.con.execute("UPDATE urls SET count = ? WHERE urls.slug = ?", (count, slug))
        self.con.commit()
