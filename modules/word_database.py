import sqlite3
import re

text_base_words = (
    "кст",
    "чд",
    "омг",
    "вайб",
    "мейт",
    "рил",
    "изи"
)

regexp_base_words = (
    r"^[ч4][e3ёе]л.?$",
    r"^[ч4][е3ёe]лих.+$",
    r"^[ч4][e3ёе]лик.+$",
    r"^[б6][эе3ё][б6][рп].?$",
    r"^[б6][эе3ё][б6][рп][я9][т7]ин.?$",
    r"^[б6][эе3ё][б6][рп]очк.+$"
    r"^сасн.+$",
    r"^абоб.+$"
    r"^амогус.+$",
    r"^рофл.+$"
)


class WordDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("databases/words.db")
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS local_words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    added_by INTEGER NOT NULL,
                    word TEXT NOT NULL,
                    type TEXT NOT NULL, 
                    UNIQUE(chat_id, word)
                )
            """)  # TYPE : regexp or text

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS global_words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    type TEXT NOT NULL,
                    UNIQUE(word)
                )
            """)  # TYPE : regexp or text

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS whitelist_words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    added_by INTEGER NOT NULL,
                    word TEXT NOT NULL,
                    UNIQUE(chat_id, word)
                )
            """)

            for word in text_base_words:
                try:
                    self.cursor.execute("INSERT INTO global_words (word, type) VALUES (?, ?)", (word, "text"))
                except sqlite3.IntegrityError:
                    pass
            
            for word in regexp_base_words:
                try:
                    self.cursor.execute("INSERT INTO global_words (word, type) VALUES (?, ?)", (word, "regexp"))
                except sqlite3.IntegrityError:
                    pass
    
    def get_all_whitelisted_words(self, chat_id):
        self.cursor.execute("SELECT word FROM whitelist_words WHERE chat_id=?", [chat_id])

        return [col[0] for col in self.cursor.fetchall()]
    
    def get_all_local_words(self, chat_id):
        self.cursor.execute("SELECT word FROM local_words WHERE chat_id=?", [chat_id])

        return [col[0] for col in self.cursor.fetchall()]

    def check_word(self, chat_id, user_word) -> bool:
        self.cursor.execute("SELECT word, type FROM global_words")

        global_words = self.cursor.fetchall()

        self.cursor.execute("SELECT word, type FROM local_words WHERE chat_id=?", [chat_id])

        local_words = self.cursor.fetchall()

        banned_words = global_words + local_words

        for column in banned_words:
            word, word_type = column
            
            if word_type == "text":
                if word == user_word:
                    if not self._check_whitelist(chat_id, word):
                        return True
            
            elif word_type == "regexp":
                if re.match(word, user_word) is not None:
                    if not self._check_whitelist(chat_id, word):
                        return True
        
        return False
    
    def add_local_word(self, chat_id: int, word: str, added_by: int, type: str):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO local_words (chat_id, added_by, word, type) VALUES (?, ?, ?, ?)",
                [chat_id, added_by, word, type]
            )
    
    def delete_local_word(self, chat_id, word):
        with self.connection:
            self.cursor.execute(
                "DELETE FROM local_words WHERE word=? AND chat_id=?",
                [word, chat_id]
            )
    
    def add_word_to_whitelist(self, chat_id, word, added_by):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO whitelist_words (chat_id, added_by, word) VALUES (?, ?, ?)",
                [chat_id, added_by, word]
            )
    
    def delete_word_from_whitelist(self, chat_id, word):
        with self.connection:
            self.cursor.execute(
                "DELETE FROM whitelist_words WHERE word=? AND chat_id=?",
                [word, chat_id]
            )
    
    def _check_whitelist(self, chat_id, word) -> bool:
        self.cursor.execute(
            "SELECT id FROM whitelist_words WHERE chat_id=? AND word=?",
            [chat_id, word]
        )

        if self.cursor.fetchone():
            return True
        return False
