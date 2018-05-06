from bootstrap.main_app import app
from flask import request
from singleton import repo, bot, slack, analytic


@app.route('/', methods=['POST', 'GET'])
def index():
    data = request.form
    with open("test.txt", "w") as files:
        files.write(str(data))
    return "Hello moto"


def outhook_test():
    data ={'token': '6aEIbL0AaoylQbD9HNSlKYDR','channel_name':'general2',
        'trigger_word':'paulinho','team_id':'TAC09TX6K', 'user_id':'UAB2X1Z7Z','user_name':'rafael.nunu2',
        'text':'paulinho: que isso ?', 'service_id':'352922744983','channel_id':'CAB2VSA7X','team_domain':'bot-pylack'}
    repo.store_message(data, 'messages')
    return True


def outhook_test_month():
    data = repo.get_last_month()
    graph_path = analytic.analyze_report_humor(data)


def outhook_test_week():
    data = repo.get_last_week()
    graph_path = analytic.analyze_report_humor(data)
    # slack service send graph


@app.route('/api/channel/outhook', methods=['POST'])
def outhook():
    repo.store_message(request.form, 'messages')
    response = bot.analyze_response(request.form['text'])
    slack.post_message(request.form['channel_id'], response)

    return "Hello moto"


# Receiving data and store a database for analytics
@app.route('/api/private/humor', methods=['POST'])
def outhook_humor():
    repo.store_message(request.form, 'daily_report')
    slack.post_message(request.form["user_id"], "Ok! Bom dia!")
    return "Hello moto"

