from backend.apis.ryanair import connected_airports, world


def test_malmo():
    airport = world().airport_by_iata("MMX")
    others = connected_airports(airport)
    assert {other.iata for other in others} == {"ZAG", "KRK", "ARN"}
