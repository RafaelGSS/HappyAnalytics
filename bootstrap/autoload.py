# import routes
from bootstrap import main_app
from routes import web, api
from singleton import bot_scheduller
import multiprocessing

def init():
    #   web.outhook_test_week()
    init_scheduller()
    main_app.app.run(debug=True)

def init_scheduller():
    multiprocessing.Process(target=bot_scheduller.run)

