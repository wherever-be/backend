from chalice import Chalice
import time
import random


app = Chalice(app_name="backend")


@app.route("/", methods=["POST"], cors=True)
def index():
    request_data = app.current_request.json_body
    time.sleep(1)
    return {
        "searchResults": [
            {
                "id": random.randint(1024, 999999),
                "destination": random.choice(["STOCKHOLM", "KRAKOW", "ROME"]),
                "goodness": random.uniform(-100, 100),
                "journeys": [
                    {
                        "friendName": random.choice(
                            ["Joshua", "Chris", "Jennifer", "Caroline"]
                        ),
                        "staysHome": False,
                        "homeToDest": {
                            "departure": {
                                "date": "2015-12-12T13:52:00.000Z",
                                "port": "ARN",
                            },
                            "arrival": {
                                "date": "2015-12-12T16:31:00.000Z",
                                "port": "BRU",
                            },
                            "price": {"amount": random.uniform(1, 100), "unit": "EUR"},
                            "bookingLink": "http://www.ryanair.com/book/coolflights.php",
                        },
                        "destToHome": {
                            "departure": {
                                "date": "2015-12-17T23:11:00.000Z",
                                "port": "BRU",
                            },
                            "arrival": {
                                "date": "2015-12-18T02:21:00.000Z",
                                "port": "NYO",
                            },
                            "price": {"amount": random.uniform(1, 100), "unit": "EUR"},
                            "bookingLink": "http://www.wizzair.com/book/otherflights.cgi",
                        },
                    }
                ],
            }
            for _ in range(5)
        ]
    }
