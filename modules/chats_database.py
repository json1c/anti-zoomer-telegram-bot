import sqlite3


class ChatsDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("databases/chats.db")
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL UNIQUE
                )  
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats_settings (
                    chat_id INTEGER NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    UNIQUE (chat_id, key)
                )                       
            """)
    
    def is_chat_exists_in_db(self, chat_id):
        self.cursor.execute(
            "SELECT id FROM chats WHERE chat_id=?",
            [chat_id]
        )
        
        return self.cursor.fetchone() is not None
    
    def insert_new_chat(self, chat_id):
        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO chats (chat_id) VALUES (?)",
                    [chat_id]
                )
                
                self.cursor.execute(
                    "INSERT INTO chats_settings VALUES (?, ?, ?)",
                    [chat_id, "admin_delete", "false"]
                )
            except sqlite3.IntegrityError:
                pass
    
    def toggle_admin_delete(self, chat_id):
        if not self.is_chat_exists_in_db(chat_id):
            self.insert_new_chat(chat_id)

        admin_delete = self.get_admin_delete(chat_id)
        
        if admin_delete:
            set_value = "false"
        else:
            set_value = "true"
        
        with self.connection:
            self.cursor.execute("""
                UPDATE chats_settings 
                SET value = ?
                WHERE chat_id = ? AND key = 'admin_delete'
            """, [set_value, chat_id]
            )
        
        return set_value
    
    def get_admin_delete(self, chat_id):
        self.cursor.execute(
            "SELECT value FROM chats_settings WHERE chat_id=? AND key='admin_delete'",
            [chat_id]
        )

        result = self.cursor.fetchone()[0]

        if result == "true":
            return True
        return False
