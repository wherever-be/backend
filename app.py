from chalice import Chalice
from chalicelib import Request


app = Chalice(app_name="backend")


@app.route("/", methods=["POST"], cors=True)
def index():
    request_data = app.current_request.json_body
    request = Request.from_frontend_json(request_data)
    response = request.response
    return response.for_frontend
