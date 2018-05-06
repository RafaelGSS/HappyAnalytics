from bootstrap.main_app import app
from flask import request, render_template
from singleton_slack import slack
from singleton import events

@app.route('/', methods=['POST', 'GET'])
def index():
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


@app.route('/templates/<section>')
def test2(section):
    return render_template(section)

@app.route('/get_template')
def test():
    return 'TROLOLO'