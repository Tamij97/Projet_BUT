import sqlite3

class Database:

    db_name = "./database.db"

    def __init__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
       
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
            '''
        )

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat (
                chat_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                user_id INTEGER NOT NULL,
                chat_title TEXT NOT NULL,
                chat_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                chat_model TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            '''
        )

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_message(
                chat_id INTEGER NOT NULL,
                chat_message_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                chat_message TEXT NOT NULL,
                chat_message_is_ia BOOLEAN NOT NULL,
                chat_message_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (chat_id) REFERENCES chat(chat_id)
            )
            '''
        )



    """
    
        USER TABLE REQUESTS

    """
    ### SELECT REQUESTS
    def select_user_by_name(self, username):
        self.cursor.execute('SELECT user_id, username, password FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def select_user_by_id(self, user_id):
        self.cursor.execute('SELECT user_id, username, password FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()

    ### DELETE REQUESTS
    def delete_user_by_name(self, username):
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        self.conn.commit()

    def delete_user_by_id(self, user_id):
        self.cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        self.conn.commit()

    ### UPDATE REQUESTS
    def update_user_username_by_id(self, user_id, username):
        self.cursor.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
        self.conn.commit()

    def update_user_password_by_id(self, user_id, password):
        self.cursor.execute('UPDATE users SET password = ? WHERE user_id = ?', (password, user_id))
        self.conn.commit()

    def update_user_password_by_name(self, username, password):
        self.cursor.execute('UPDATE users SET password = ? WHERE username = ?', (password, username))
        self.conn.commit()

    def update_user_username_by_id(self, user_id, username):
        self.cursor.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
        self.conn.commit()

    ### INSERT REQUESTS
    def insert_user(self, username, password):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    ### CUSTOM REQUESTS
    def user_exists(self, username):
        self.cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
        exists = self.cursor.fetchone() is not None
        return exists




    """
    
        Chat TABLE REQUESTS

    """
    ### SELECT REQUESTS
    def select_chat_by_id(self, chat_id):
        self.cursor.execute('SELECT chat_id, user_id, chat_title, chat_date, chat_model FROM chat WHERE chat_id = ?', (chat_id,))
        return self.cursor.fetchone()
    
    def select_chat_by_user_id(self, user_id):
        self.cursor.execute('SELECT chat_id, user_id, chat_title, chat_date, chat_model FROM chat WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()
    
    def select_chat_by_title(self, chat_title):
        self.cursor.execute('SELECT chat_id, user_id, chat_title, chat_date, chat_model FROM chat WHERE chat_title = ?', (chat_title,))
        return self.cursor.fetchone()
    
    ### DELETE REQUESTS
    def delete_chat_by_id(self, chat_id):
        self.cursor.execute('DELETE FROM chat WHERE chat_id = ?', (chat_id,))
        self.conn.commit()

    def delete_chat_by_user_id(self, user_id):
        self.cursor.execute('DELETE FROM chat WHERE user_id = ?', (user_id,))
        self.conn.commit()

    def delete_chat_by_title(self, chat_title):
        self.cursor.execute('DELETE FROM chat WHERE chat_title = ?', (chat_title,))
        self.conn.commit()

    ### UPDATE REQUESTS
    def update_chat_title_by_id(self, chat_id, chat_title):
        self.cursor.execute('UPDATE chat SET chat_title = ? WHERE chat_id = ?', (chat_title, chat_id))
        self.conn.commit()
    
    def update_chat_title_by_user_id(self, user_id, chat_title):
        self.cursor.execute('UPDATE chat SET chat_title = ? WHERE user_id = ?', (chat_title, user_id))
        self.conn.commit()

    def update_chat_title_by_title(self, chat_title, new_chat_title):
        self.cursor.execute('UPDATE chat SET chat_title = ? WHERE chat_title = ?', (new_chat_title, chat_title))
        self.conn.commit()

    ### INSERT REQUESTS
    def insert_chat(self, user_id, chat_title, chat_model):
        self.cursor.execute("INSERT INTO chat (user_id, chat_title, chat_date, chat_model) VALUES (?, ?, datetime('now'), ?) RETURNING chat_id", (user_id, chat_title, chat_model))
        chat_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return chat_id
    
    ### CUSTOM REQUESTS
    def select_chat_by_id_and_user_id(self, chat_id, user_id):
        self.cursor.execute('SELECT chat_id, user_id, chat_title, chat_date, chat_model FROM chat WHERE chat_id = ? AND user_id = ?', (chat_id, user_id))
        return self.cursor.fetchone()
    
    def select_all_user_chats(self, user_id):
        self.cursor.execute('SELECT chat_id, chat_title, chat_date, chat_model FROM chat WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

    def delete_chat_by_id_and_by_user_id(self, chat_id, user_id):
        self.cursor.execute('DELETE FROM chat WHERE chat_id = ? AND user_id = ?', (chat_id, user_id))
        self.conn.commit()



    """
    
        chat_message TABLE REQUESTS

    """
    ### SELECT REQUESTS
    def select_chat_message_by_chat_id(self, chat_id):
        self.cursor.execute('SELECT chat_id, chat_message_id, chat_message, chat_message_is_ia, chat_message_date FROM chat_message WHERE chat_id = ?', (chat_id,))
        return self.cursor.fetchall()
    
    def select_chat_message_by_chat_message_id(self, chat_message_id):
        self.cursor.execute('SELECT chat_id, chat_message_id, chat_message, chat_message_is_ia, chat_message_date FROM chat_message WHERE chat_message_id = ?', (chat_message_id,))
        return self.cursor.fetchone()
    
    def select_chat_message_by_chat_message(self, chat_message):
        self.cursor.execute('SELECT chat_id, chat_message_id, chat_message, chat_message_is_ia, chat_message_date FROM chat_message WHERE chat_message = ?', (chat_message,))
        return self.cursor.fetchone()
    
    ### DELETE REQUESTS
    def delete_chat_message_by_chat_id(self, chat_id):
        self.cursor.execute('DELETE FROM chat_message WHERE chat_id = ?', (chat_id,))
        self.conn.commit()
    
    def delete_chat_message_by_chat_message_id(self, chat_message_id):
        self.cursor.execute('DELETE FROM chat_message WHERE chat_message_id = ?', (chat_message_id,))
        self.conn.commit()

    def delete_chat_message_by_chat_message(self, chat_message):
        self.cursor.execute('DELETE FROM chat_message WHERE chat_message = ?', (chat_message,))
        self.conn.commit()

    ### UPDATE REQUESTS
    def update_chat_message_by_chat_message_id(self, chat_message_id, chat_message):
        self.cursor.execute('UPDATE chat_message SET chat_message = ? WHERE chat_message_id = ?', (chat_message, chat_message_id))
        self.conn.commit()
    
    def update_chat_message_by_chat_message(self, chat_message, new_chat_message):
        self.cursor.execute('UPDATE chat_message SET chat_message = ? WHERE chat_message = ?', (new_chat_message, chat_message))
        self.conn.commit()
    
    ### INSERT REQUESTS
    def insert_chat_message(self, chat_id, chat_message, chat_message_is_ia):
        self.cursor.execute('INSERT INTO chat_message (chat_id, chat_message, chat_message_is_ia) VALUES (?, ?, ?)', (chat_id, chat_message, chat_message_is_ia))
        self.conn.commit()
    
    def select_chat_message_by_chat_id_and_user_id(self, chat_id, user_id):
        self.cursor.execute('SELECT chat_message_id, chat_message, chat_message_is_ia, chat_message_date FROM chat_message JOIN chat ON chat_message.chat_id = chat.chat_id WHERE chat_message.chat_id = ? AND chat.user_id = ?', (chat_id, user_id))
        return self.cursor.fetchall()

    

    def begin_transaction(self):
        self.conn.execute('BEGIN')

    def commit_transaction(self):
        self.conn.commit()

    def rollback_transaction(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()