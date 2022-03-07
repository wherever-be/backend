from aiohttp import web
from backend import Request


async def handler(request):
    request_data = await request.json()
    request = Request.from_frontend_json(request_data)
    response = request.response
    return web.json_response(response.frontend_json)


app = web.Application()
app.add_routes([web.post("/", handler)])  # TODO: CORS
web.run_app(app)
