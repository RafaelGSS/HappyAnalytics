from bootstrap.main_app import app


@app.route('/')
def index():
    return 'Hello worlds!'