from datetime import date

from backend import Query


def test_from_frontend_json():
    query = Query.from_frontend_json(
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
    assert query.time_frame.start_date == date(2022, 3, 5)
    assert query.time_frame.end_date == date(2022, 6, 19)
    assert query.min_days == 3
    assert query.max_days == 7
    assert len(query.friends) == 3
    assert query.destination_country.code == "fr"
    assert query.destination_city.code == "PARIS"
