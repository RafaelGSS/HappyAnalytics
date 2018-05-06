from app.bot.funny_bot import FunnyBot
from app.service.analytics import Analytic
from app.bot.botscheduler import BotScheduler
from app.service.events import Events

events = Events()
bot_scheduller = BotScheduler()
bot = FunnyBot()
analytic = Analytic()