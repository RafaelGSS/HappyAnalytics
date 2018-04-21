# import routes
from bootstrap import main_app
from routes import web, api


def init():
    main_app.app.run(debug=True)


