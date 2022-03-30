from ratelimit import limits, sleep_and_retry
import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    wait_exponential,
    wait_fixed,
    wait_fixed,
)


from backend.apis.errors import (
    TooManyRequestsError,
    DownForMaintenanceError,
    print_exception,
)
from .errors import RyanairAPIError


@retry(
    retry=retry_if_exception_type(TooManyRequestsError),
    wait=wait_exponential(),
    before_sleep=print_exception,
)
@retry(
    retry=retry_if_exception_type(DownForMaintenanceError),
    wait=wait_fixed(10),
    before_sleep=print_exception,
)
@retry(
    retry=retry_if_exception_type(requests.ConnectionError),
    wait=wait_fixed(10),
    before_sleep=print_exception,
)
@sleep_and_retry
@limits(calls=10, period=1)
def make_request(url: str, parameters):
    request = requests.get(url, params=parameters)
    if request.status_code == 429:
        raise TooManyRequestsError()
    if request.status_code != 200:
        raise RyanairAPIError(request.status_code)
    if "Our website is undergoing essential maintenance" in request.text:
        raise DownForMaintenanceError()
    return request.json()
