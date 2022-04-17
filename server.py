from backend import background_poll_loop, ExpiringCache, Query, search
from datetime import timedelta
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
    with ExpiringCache.duration(timedelta(hours=12)):
        query = Query.from_frontend_json(request_data)
        results = search(query)
    return results.frontend_json
