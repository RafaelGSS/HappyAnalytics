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


@app.route('/api/outhook', methods=['POST'])
def outhook():
    repo.store_message(request.form)
    response = bot.analyze_response(request.form['text'])
    slack.post_message(request.form['channel_id'], response)

    return "Hello moto"

# STORE IN DATABASE
# ANALITICS
# RESPONSE MESSAGE

@app.route('/api/private/humor')
# Receiving data and store a database for analytics
def outhook_humor():
    pass


def check_token():
    # VERIFY IN ENV
    pass