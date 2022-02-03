import requests
import datetime
from flight_data import FlightData

TEQUILA_ENDPOINT = "<you endpoint>"
TEQUILA_API_KEY = "<your api key>"

header = {
    "apikey": TEQUILA_API_KEY
}


class FlightSearch:

    def get_destination_code(self, city_name):
        parameter = {
            "term": city_name,
        }

        r = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query", headers=header, params=parameter)
        code = r.json()["locations"][0]["code"]
        return code


    def check_flights(self, fly_loc, fly_to, date_now, future_date):
        parameter = {
            "fly_from": fly_loc,
            "fly_to": fly_to,
            "date_from": date_now,
            "date_to": future_date,
            "flight_type": "round",
            "curr": "GBP",
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "max_stopovers": 0,
            "one_for_city": 1,

        }
        r = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=header, params=parameter)
        try:
            data = r.json()["data"][0]
        except IndexError:
            parameter["max_stopovers"] = 1
            r = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=header, params=parameter)
            try:
                data = r.json()['data'][0]
            except IndexError:
                print(f"No flights found for {fly_to}.")
                return None
            else:
                flight_data = FlightData(
                    price=data['price'],
                    origin_city=data['route'][0]['cityFrom'],
                    origin_airport=data['route'][0]['flyFrom'],
                    destination_city=data['route'][0]['cityTo'],
                    destination_airport=data['route'][0]['flyTo'],
                    out_date=data['route'][0]['local_departure'].split('T')[0],
                    return_date=data['route'][1]['local_departure'].split('T')[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                print(f"{flight_data.destination_city}: £{flight_data.price}")
                return flight_data
        else:
            flight_data = FlightData(
                price=data['price'],
                origin_city=data['route'][0]['cityFrom'],
                origin_airport=data['route'][0]['flyFrom'],
                destination_city=data['route'][0]['cityTo'],
                destination_airport=data['route'][0]['flyTo'],
                out_date=data['route'][0]['local_departure'].split('T')[0],
                return_date=data['route'][1]['local_departure'].split('T')[0],
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
