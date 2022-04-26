import sqlite3

base_words = (
    "чел",
    "кринж",
    "лол",
    "кринжатина",
    "пчел",
    "гетать",
    "гетаю",
    "слит",
    "бебра",
    "бэбра",
    "абоба",
    "абобус",
    "брух",
    "чела",
    "челов",
    "челы",
    "челу",
    "беброчка",
    "бебрятина",
    "бебрятину",
    "бебрятины",
    "кринге",
    "чд",
    "кст",
    "амогус",
    "сасный",
    "сасная",
    "zxc",
    "дноклы",
    "дноклов",
    "краш",
    "изи",
    "рил",
    "рофл",
    "рофлить",
    "рофлю",
    "омг",
    "флекс",
    "челиха",
    "чувиха",
    "челик",
    "форсить",
    "хайп",
    "форс",
    "чилить",
    "жиза",
    "пруфы",
    "баттхерт",
    "вайб",
    "зашквар",
    "крипово",
    "кринжулька",
    "мейт",
    "пранк"
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
                    UNIQUE(chat_id, word)
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS global_words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    UNIQUE(word)
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS whitelist_words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    added_by INTEGER NOT NULL,
                    word TEXT NOT NULL,
                    UNIQUE(chat_id, word)
                )
            """)

            for word in base_words:
                try:
                    self.cursor.execute("INSERT INTO global_words (word) VALUES (?)", (word,))
                except sqlite3.IntegrityError:
                    pass
    
    def get_all_whitelisted_words(self, chat_id):
        self.cursor.execute("SELECT word FROM whitelist_words WHERE chat_id=?", [chat_id])

        return [col[0] for col in self.cursor.fetchall()]
    
    def get_all_local_words(self, chat_id):
        self.cursor.execute("SELECT word FROM local_words WHERE chat_id=?", [chat_id])

        return [col[0] for col in self.cursor.fetchall()]

    def check_word(self, chat_id, user_word) -> bool:
        self.cursor.execute("SELECT word FROM global_words")

        global_words = self.cursor.fetchall()

        self.cursor.execute("SELECT word FROM local_words WHERE chat_id=?", [chat_id])

        local_words = self.cursor.fetchall()

        banned_words = global_words + local_words

        for word in banned_words:
            if word[0] == user_word:
                if not self._check_whitelist(chat_id, word[0]):
                    return True
        
        return False
    
    def add_local_word(self, chat_id, word, added_by):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO local_words (chat_id, added_by, word) VALUES (?, ?, ?)",
                [chat_id, added_by, word]
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
