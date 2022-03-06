from datetime import date, timedelta

from chalicelib import Request
from chalicelib.time_frame import TimeFrame
from chalicelib.friend import Friend
from chalicelib.scraper import world


def test_from_frontend_json():
    request = Request.from_frontend_json(
        {
            "timeFrame": {"start": "2022-03-05", "end": "2022-06-19"},
            "durationRange": {"min": 3, "max": 7},
            "friends": [
                {"name": "Julian", "city": "HAMBURG"},
                {"name": "Nick", "city": "KRAKOW"},
                {"name": "Lukas", "city": "BRUSSELS"},
            ],
            "destination": {"country": "fr", "city": "PARIS"},
        }
    )
    assert request.time_frame.start_date == date(2022, 3, 5)
    assert request.time_frame.end_date == date(2022, 6, 19)
    assert request.min_days == 3
    assert request.max_days == 7
    assert len(request.friends) == 3
    assert request.destination_country.code == "fr"
    assert request.destination_city.code == "PARIS"


def test_simple_search():
    request = Request(
        time_frame=TimeFrame(
            start_date=date.today(), end_date=date.today() + timedelta(days=14)
        ),
        min_days=3,
        max_days=7,
        friends=[
            Friend(
                name="Jake",
                city=world().city_by_code("STOCKHOLM"),
            )
        ],
        destination_country=world().country_by_code("it"),
        destination_city=world().city_by_code("ROME"),
    )
    response = request.response
    assert len(response.trips) >= 1
