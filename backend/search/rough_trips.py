from backend.apis import rough_connections
from backend.friend import Friend
from backend.geography import City
from backend.journey import Journey
from backend.query import Query
from backend.time_frame import TimeFrame
from backend.trip import Trip
from .pick_varied import pick_varied


def rough_trips(query: Query):
    candidates = [
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
    return pick_varied(candidates, max_trips=query.max_trips)


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
