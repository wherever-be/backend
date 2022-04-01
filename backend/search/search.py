from backend.results import Results
from .precise_trips import precise_trips


def search(query):
    return Results(trips=precise_trips(query))
