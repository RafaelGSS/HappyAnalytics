from app.repository.repository import Repository
from app.bot.funny_bot import FunnyBot
from app.service.slack import Slack
from app.service.analytics import Analytic
from app.bot.botscheduler import BotScheduler

bot_scheduller = BotScheduler()
repo = Repository()
bot = FunnyBot()
slack = Slack()
analytic = Analytic()