from typing import List

from backend.apis import rough_connections, precise_connections
from backend.geography import City
from .friend import Friend
from .journey import Journey
from .query import Query
from .results import Results
from .time_frame import TimeFrame
from .trip import Trip


def search(query, max_trips=64):
    return Results(trips=precise_trips(query, max_trips=max_trips))


def precise_trips(query, max_trips: int):
    base_trips = pick_varied(candidates=rough_trips(query), max_trips=max_trips * 2)
    expanded = [
        combined
        for base_trip in base_trips
        for combined in Trip.combine_journeys(
            destination=base_trip.destination,
            journeys=[
                [
                    Journey(
                        friend=base_journey.friend,
                        home_to_destination=home_to_destination,
                        destination_to_home=destination_to_home,
                    )
                    for home_to_destination in precise_connections(
                        num_people=1,  # TODO: group people
                        flight_date=base_journey.home_to_destination.departure.date(),
                        origin=base_journey.home_to_destination.from_airport,
                        destination=base_journey.home_to_destination.to_airport,
                    )
                    for destination_to_home in precise_connections(
                        num_people=1,  # TODO: group people
                        flight_date=base_journey.destination_to_home.departure.date(),
                        origin=base_journey.destination_to_home.from_airport,
                        destination=base_journey.destination_to_home.to_airport,
                    )
                ]
                for base_journey in base_trip.journeys
            ],
        )
    ]
    return pick_varied(candidates=expanded, max_trips=max_trips)


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


def pick_varied(candidates: List[Trip], max_trips: int):
    """A list of trips, limited to a sensible number, picked based on goodnes and variety"""
    results: List[Trip] = []

    def variety_score(trip: Trip):
        if len(results) == 0:
            return trip.goodness
        return trip.goodness - max(result.similarity(trip) for result in results)

    for _ in range(max_trips):
        if len(candidates) == 0:
            break
        best_candidate = max(candidates, key=variety_score)
        candidates.remove(best_candidate)
        results.append(best_candidate)
    return results
