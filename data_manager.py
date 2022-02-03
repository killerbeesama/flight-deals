import requests

SHEETY_ENDPOINT = "<you endpoint>"
SHEETY_API = "<your api key>"

sheety_header = {
    "Authorization": f"Bearer {SHEETY_API}"
}


class DataManager:
    def __init__(self):
        self.destination_data = {}


    def read_data(self):
        r = requests.get(url=SHEETY_ENDPOINT, headers=sheety_header)
        data = r.json()
        self.destination_data = data["prices"]
        return self.destination_data


    def update_sheet_data(self):
        for i in self.destination_data:
            sheety_update_endpoint = f"{SHEETY_ENDPOINT}/{i['id']}"
            sheety_parameter = {
                "price": {
                    "iataCode": i['iataCode']
                }
            }
            r = requests.put(url=sheety_update_endpoint, headers=sheety_header, json=sheety_parameter)
            # print(r.json())
