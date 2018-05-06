from bootstrap.main_app import app
from flask import request
from singleton_slack import slack
from singleton_repo import repo
from singleton import analytic, events


@app.route('/', methods=['POST', 'GET'])
def index():
    # url_verification
    #with open('text.txt', 'w') as file:
     #   file.write(request.get_json())

    if request.method == 'GET':
        return request.args.get('challenge')

    json = request.get_json()
    if json.get('challenge') is not None:
        return json.get('challenge')

    formated = slack.get_message_formated(request.get_json())
    print(formated)
    if formated is not False:
        event = events.analyze_message(formated)
        if event is False:
            return 'NOT CALL BOT'
        response = event(formated)
        return slack.post_message(formated['channel'], response)

    return 'IS NOT MESSAGE VALID!'


# @app.route('/api/channel/outhook', methods=['POST'])
# def outhook():
#     repo.store_message(request.form, 'messages')
#     response = bot.analyze_response(request.form['text'])
#     slack.post_message(request.form['channel_id'], response)
#
#     return "Hello moto"


# Receiving data and store a database for analytics
@app.route('/api/private/humor', methods=['POST'])
def outhook_humor():
    repo.store_message(request.form, 'daily_report')
    slack.post_message(request.form["user_id"], "Ok! Bom dia!")
    return "Hello moto"

