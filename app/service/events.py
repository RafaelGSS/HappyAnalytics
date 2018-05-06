import env
from app.bot.funny_bot import FunnyBot
from singleton_repo import repo
from singleton_slack import slack
from singleton_analytic import analytic
import re

bot = FunnyBot()
# NAME_BOT: humor {note} {description}
# NAME_BOT: meme {type}

class Events(object):

    def __init__(self):
        self.trigger_humor = 'humor'.format(env.NAME_BOT)
        self.trigger_meme = 'meme'.format(env.NAME_BOT)
        self.trigger_analytic = 'analise'
        self.triggers = {
            self.trigger_humor: self.store_humor,
            self.trigger_meme: self.get_meme,
            self.trigger_analytic: self.send_analytic_week
        }

    def send_analytic_week(self, message):
        data = repo.get_last_week()
        analize_path = analytic.analyze_report_humor(data)
        return '{}/{}'.format(env.APP_URL, analize_path)

    def store_humor(self, message):
        data = message['message'].split(self.trigger_humor)[1] # Get message after NAME_BOT: humor
        formated = data.split(' ')
        if len(formated) < 1:
            return 'Ops! Para salvar seu humor diario voce precisa mandar assim: {}: humor [sua nota de 0 a 5] [descricao sobre sua nota(opcional)]'.format(env.NAME_BOT)

        note = formated[0]
        description = formated[1] if len(formated) > 1 else ''
        repo.store_report('daily_report', message['user_id'], note, description)

        return 'Ok! Obrigado!'

    def get_meme(self, message):
        data = message['message'].split(self.trigger_meme)[1]
        meme = bot.analyze_response(data)
        return meme['link']

    # analyze if contains trigger words
    # each trigger word have a function to execute

    def analyze_message(self, data):

        trigger = self.valid_message(data['message'])
        return trigger

    def valid_message(self, message):
        check_meme = re.search(self.trigger_meme, message)
        check_humor = re.search(self.trigger_humor, message)
        check_analytic = re.search(self.trigger_analytic, message)

        if check_humor is not None:
            return self.triggers[self.trigger_humor]

        if check_meme is not None:
            return self.triggers[self.trigger_meme]

        if check_analytic is not None:
            return self.triggers[self.trigger_analytic]

        return False
