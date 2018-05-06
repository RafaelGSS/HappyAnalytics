from bootstrap.main_app import app
from flask import request, render_template
from singleton import events
from flask import jsonify
import datetime


@app.route('/humor', methods=['POST'])
def humor():
    data = request.form
    event = events.triggers[events.trigger_humor]
    return event(data['text'], data['user_id'], data['user_name'])


@app.route('/meme/all', methods=['POST'])
def mem_all():
    data = request.form
    event = events.triggers[events.trigger_meme]
    response = event(data['text'])
    return jsonify({
        "text": response['link'],
        "attachments": [{
            "image_url": response['image'],
            "thumb_url": response['image'],
            "footer": "Slack API",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
        }]})


@app.route('/analytic', methods=['POST'])
def analytic():
    event = events.triggers[events.trigger_analytic]
    return event(image_name='templates/analyze_{}.html'.format(datetime.date.today()), message='')


@app.route('/templates/<section>')
def test2(section):
    return render_template(section)
