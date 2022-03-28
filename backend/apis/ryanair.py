from ratelimit import limits, RateLimitException
import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    wait_exponential,
    wait_fixed,
    RetryCallState,
    wait_fixed,
)


class TooManyRequestsError(Exception):
    pass


class DownForMaintenanceError(Exception):
    pass


class RyanairAPIError(Exception):
    def __init__(self, code: int):
        super().__init__()
        self.code = code


def warn_on_exception(retry_state: RetryCallState):
    print(f"{retry_state.fn.__name__} produced {retry_state.outcome.exception()}")


@retry(
    retry=retry_if_exception_type(TooManyRequestsError),
    wait=wait_exponential(),
    before_sleep=warn_on_exception,
)
@retry(
    retry=retry_if_exception_type(DownForMaintenanceError),
    wait=wait_fixed(10),
    before_sleep=warn_on_exception,
)
@retry(
    retry=retry_if_exception_type(requests.ConnectionError),
    wait=wait_fixed(10),
    before_sleep=warn_on_exception,
)
@retry(
    retry=retry_if_exception_type(RateLimitException),
    wait=wait_fixed(1),
)
@limits(calls=1, period=1)
def make_request(url: str, parameters):
    request = requests.get(url, params=parameters)
    if request.status_code == 429:
        raise TooManyRequestsError()
    if request.status_code != 200:
        raise RyanairAPIError(request.status_code)
    if "Our website is undergoing essential maintenance" in request.text:
        raise DownForMaintenanceError()
    return request.json()
