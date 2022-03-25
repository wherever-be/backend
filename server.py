from backend import background_poll_loop, Request
from flask import Flask, request as flask_request
from flask_cors import cross_origin
from flask_talisman import Talisman


app = Flask(__name__)
Talisman(app)
background_poll_loop()


@app.route("/", methods=["POST"])
@cross_origin()
def handler():
    request_data = flask_request.get_json()
    request = Request.from_frontend_json(request_data)
    response = request.response
    return response.frontend_json