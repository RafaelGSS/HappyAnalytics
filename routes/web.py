from bootstrap.main_app import app
from flask import request


@app.route('/', methods=['POST', 'GET'])
def index():
    data = request.form
    with open("test.txt", "w") as files:
        files.write(str(data))
    return "Hello moto"


@app.route('/api/outhook', methods=['POST', 'GET'])
def outhook():
    data = request.form
    with open("test.txt", "w") as files:
        files.write(str(data))

    #POST MESSAGE SERVICE SLACK AND STORE IN DATABASE
    return "Hello moto"


@app.route('/api/private/humor')
# Receiving data and store a database for analytics
def outhook_humor():
    pass


def check_token():
    # VERIFY IN ENV
    pass