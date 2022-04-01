from backend.apis import precise_connections, RyanairBlacklistError
from backend.journey import Journey
from backend.query import Query
from backend.trip import Trip
from .pick_varied import pick_varied
from .rough_trips import rough_trips


def precise_trips(query: Query, max_trips: int):
    _rough_trips = rough_trips(query, max_trips=max_trips)
    try:
        _precise_trips = [
            combined
            for rough_trip in _rough_trips
            for combined in Trip.combine_journeys(
                destination=rough_trip.destination,
                journeys=[
                    precise_journeys(rough_journey)
                    for rough_journey in rough_trip.journeys
                ],
            )
        ]
    except RyanairBlacklistError:
        return _rough_trips
    return pick_varied(candidates=_precise_trips, max_trips=max_trips)


def precise_journeys(rough_journey: Journey):
    return [
        Journey(
            friend=rough_journey.friend,
            home_to_destination=home_to_destination,
            destination_to_home=destination_to_home,
        )
        for home_to_destination in precise_connections(
            num_people=1,  # TODO: group people
            flight_date=rough_journey.home_to_destination.departure.date(),
            origin=rough_journey.home_to_destination.from_airport,
            destination=rough_journey.home_to_destination.to_airport,
        )
        for destination_to_home in precise_connections(
            num_people=1,  # TODO: group people
            flight_date=rough_journey.destination_to_home.departure.date(),
            origin=rough_journey.destination_to_home.from_airport,
            destination=rough_journey.destination_to_home.to_airport,
        )
    ]
