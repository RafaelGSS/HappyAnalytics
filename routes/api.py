from bootstrap.main_app import app


@app.route('/api/v1')
def api_index():
    return 'Hello worlds!'