from backend.apis import connected_airports, world


def test_olsztyn():
    airport = world().airport_by_iata("SZY")
    others = connected_airports(airport)
    assert {other.iata for other in others} == {"WRO", "STN"}
