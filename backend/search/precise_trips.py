from backend.apis import precise_connections
from backend.journey import Journey
from backend.query import Query
from backend.trip import Trip
from .pick_varied import pick_varied
from .rough_trips import rough_trips


def precise_trips(query: Query):
    expanded = [
        combined
        for rough_trip in rough_trips(query)
        for combined in Trip.combine_journeys(
            destination=rough_trip.destination,
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
                for base_journey in rough_trip.journeys
            ],
        )
    ]
    return pick_varied(candidates=expanded, max_trips=query.max_trips)
