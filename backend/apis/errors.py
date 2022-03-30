from tenacity import RetryCallState


class TooManyRequestsError(Exception):
    pass


class DownForMaintenanceError(Exception):
    pass


def print_exception(retry_state: RetryCallState):
    print(f"{retry_state.fn.__name__} produced {repr(retry_state.outcome.exception())}")
