from backend import background_poll_loop, Request
from flask import Flask, request as flask_request
from flask_cors import cross_origin


app = Flask(__name__)


@app.route("/", methods=["POST"])
@cross_origin()
def handler():
    request_data = flask_request.get_json()
    request = Request.from_frontend_json(request_data)
    response = request.response
    return response.frontend_json


background_poll_loop()
app.run(host="0.0.0.0", port=80, debug=False)
