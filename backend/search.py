from typing import List

from backend.apis import rough_connections
from backend.geography import City
from .friend import Friend
from .journey import Journey
from .query import Query
from .results import Results
from .time_frame import TimeFrame
from .trip import Trip


def search(query):
    return Results(trips=limited_trips(query))


def limited_trips(query: Query, max_trips=64) -> List[Trip]:
    """A list of trips, limited to a sensible number, picked based on goodnes and variety"""
    results: List[Trip] = []

    def variety_score(trip: Trip):
        if len(results) == 0:
            return trip.goodness
        return trip.goodness - max(result.similarity(trip) for result in results)

    candidates = rough_trips(query)
    for _ in range(max_trips):
        if len(candidates) == 0:
            break
        best_candidate = max(candidates, key=variety_score)
        candidates.remove(best_candidate)
        results.append(best_candidate)
    return results


def rough_trips(query: Query):
    return [
        trip
        for trip_dates in query.trip_dates
        for destination in query.destination_cities
        for trip in Trip.combine_journeys(
            destination=destination,
            journeys=[
                rough_journeys(
                    friend=friend,
                    trip_dates=trip_dates,
                    destination=destination,
                )
                for friend in query.friends
            ],
        )
    ]


def rough_journeys(friend: Friend, trip_dates: TimeFrame, destination: City):
    return [
        Journey(
            friend=friend,
            home_to_destination=home_to_destination,
            destination_to_home=destination_to_home,
        )
        for home_airport in friend.city.airports
        for destination_airport in destination.airports
        for home_to_destination in rough_connections(
            origin=home_airport,
            destination=destination_airport,
            flight_date=trip_dates.start_date,
        )
        for destination_to_home in rough_connections(
            origin=destination_airport,
            destination=home_airport,
            flight_date=trip_dates.end_date,
        )
    ]
