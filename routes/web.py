from bootstrap.main_app import app
from app.repository.repository import Repository
from app.bot.funny_bot import FunnyBot
from app.service.slack import Slack
from flask import request

# Dependencies Injection latter.
repo = Repository()
bot = FunnyBot()
slack = Slack()


@app.route('/', methods=['POST', 'GET'])
def index():
    data = request.form
    with open("test.txt", "w") as files:
        files.write(str(data))
    return "Hello moto"


def outhook_test():
    data ={'token': '6aEIbL0AaoylQbD9HNSlKYDR','channel_name':'general',
        'trigger_word':'paulinho','team_id':'TAC09TX6K', 'user_id':'UAB2X1Z7F','user_name':'rafael.nunu',
        'text':'paulinho: que isso ?', 'service_id':'352922744983','channel_id':'CAB2VSA7P','team_domain':'bot-pylack'}
    repo.store_message(data, 'messages')
    return True


@app.route('/api/channel/outhook', methods=['POST'])
def outhook():
    repo.store_message(request.form, 'messages')
    response = bot.analyze_response(request.form['text'])
    slack.post_message(request.form['channel_id'], response)

    return "Hello moto"


@app.route('/api/private/humor', methods=['POST'])
# Receiving data and store a database for analytics
def outhook_humor():
    repo.store_message(request.form, 'messages')
    slack.post_message(request.form["user_id"], "Ok! Bom dia!")
    return "Hello moto"

