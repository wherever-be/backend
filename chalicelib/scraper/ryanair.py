import requests


# TODO: retry on some errors, throttle
def make_request(url: str, parameters):
    request = requests.get(url, params=parameters)
    if request.status_code == 429:
        raise TooManyRequestsError()
    if request.status_code != 200:
        raise RyanairAPIError(request.status_code)
    return request.json()


class TooManyRequestsError(Exception):
    pass


class RyanairAPIError(Exception):
    def __init__(self, code: int):
        super().__init__()
        self.code = code
