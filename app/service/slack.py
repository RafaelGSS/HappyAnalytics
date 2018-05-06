import requests
import env


class Slack(object):
    def __init__(self):
        pass

    def post_message(self, channel_id, message):
        status = requests.post(env.POST_MESSAGE_URL, data={
            'token': env.SLACK_TOKEN,
            'channel': channel_id,
            'text': message
        }, headers={'Authorization': 'Bearer {}'.format(env.SLACK_TOKEN)})

        if status.status_code == 200:
            return 'OK'

        return 'Post error'

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

