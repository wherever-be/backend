from datetime import date

from chalicelib import Request


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
