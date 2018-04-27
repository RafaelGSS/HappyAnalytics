from app.database.db import DB
import time


class Repository(object):
    def __init__(self):
        self.db = DB()
        
    def store_message(self, form, table):
        self.insert_user(form['user_id'])
        self.insert_channel(form['channel_id'])
        data = { 
            'user_id': form['user_id'],
            'channel_id': form['channel_id'],
            'trigger_word': form['trigger_word'],
            'text': form['text'],
            'token': form['token']
        }
        self.db.insert_test(table, data)

        return True

    def create_or_update(self):
        pass
    
    def insert_user(self, user_id):
        pass
    
    def insert_channel(self, channel_id):
        pass
