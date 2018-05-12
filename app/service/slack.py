class Slack(object):
    def __init__(self):
        pass

    def send_message_users(self):
        pass

    def get_message_formated(self, data):
        if data['event']['type'] != 'message':
            return False
        if data['event'].get('user') is None:
            return False

        formated = {
            'message': data['event']['text'],
            'user_id': data['event']['user'],
            'channel': data['event']['channel'],
            'channel_type': data['event']['channel_type']
        }

        return formated

