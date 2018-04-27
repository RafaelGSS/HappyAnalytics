# import routes
from bootstrap import main_app
from routes import web, api


def init():
    web.outhook_test()
    #main_app.app.run(debug=True)


