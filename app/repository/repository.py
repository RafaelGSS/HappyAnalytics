from app.database.db import DB
import datetime


class Repository(object):
    def __init__(self):
        self.db = DB()

    def store_report(self, table, user_id, description, note, check_token=False):
        user = self.insert_user(user_id, '')
        data = {
            'user_id': user_id,
            'note_humor': note,
            'description': description,
            'date': str(datetime.date.today())
        }
        message = self.db.insert_data(table, data)
        return True if user and message else False

    def store_message(self, form, table, check_token=True):
        if check_token and not self.check_token(form['token']):
            return False

        user = self.insert_user(form['user_id'], form['user_name'])
        channel = self.insert_channel(form['channel_id'], form['channel_name'])
        data = { 
            'user_id': form['user_id'],
            'channel_id': form['channel_id'],
            'trigger_word': form['trigger_word'],
            'text': form['text'],
            'token': form['token']
        }
        message = self.db.insert_data(table, data)
        return True if user and channel and message else False
    
    def insert_user(self, user_id, user_name):
        exist = self.db.select('users', where="user_id=\'{}\'".format(user_id))
        if exist:
            return True
        return self.db.insert_data('users', {'user_id': '{}'.format(user_id),
                                             'user_name': '{}'.format(user_name)})

    def insert_channel(self, channel_id, channel_name):
        exist = self.db.select('channels', where='channel_id=\'{}\''.format(channel_id))
        if exist:
            return True
        return self.db.insert_data('channels', {'channel_id': '{}'.format(channel_id),
                                                'channel_name': '{}'.format(channel_name)})

    def check_token(self, token):
        token = self.db.select('tokens', where='token=\'{}\''.format(token))
        if token:
            return True
        return False

    def get_last_week(self):
        week = self.db.select('daily_report', where='date > DATE(NOW() - INTERVAL 7 DAY) AND date <= DATE(NOW())')
        return week

    def get_last_month(self):
        month = self.db.select('daily_report', where='date > DATE(NOW() - INTERVAL 30 DAY) AND date <= DATE(NOW())')
        return month

    def get_memes(self, args_gen=''):
        memes = self.db.select('posts', args=args_gen)
        return memes

    def update_count_meme(self, id, set):
        self.db.update('posts', where='id=\'{}\''.format(id), set='counter={}'.format(set))
        return True