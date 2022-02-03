from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
import datetime

EMAIL = "<your email>"
PASSWORD = "<your password>"


TRAVEL_LOCATION_FROM = "<your location>"

dt_now = datetime.datetime.now()
current_date_now = dt_now.strftime(f"{'%d'}/{'%m'}/{'%Y'}")
six_months_from_now = (dt_now + datetime.timedelta(days=6 * 30)).strftime(f"{'%d'}/{'%m'}/{'%Y'}")

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager(EMAIL,PASSWORD)

sheet_data = data_manager.read_data()

if sheet_data[0]["iataCode"] == "":
    for i in sheet_data:
        i['iataCode'] = flight_search.get_destination_code(i['city'])
    data_manager.destination_data = sheet_data
    data_manager.update_sheet_data()

for i in sheet_data:
    fly_to = i['iataCode']
    history_price = i['lowestPrice']
    flight_data = flight_search.check_flights(TRAVEL_LOCATION_FROM, fly_to, current_date_now, six_months_from_now)
    if flight_data == None:
        pass
    else:
        if flight_data.price < history_price:
            price = flight_data.price
            departure_city_name = flight_data.origin_city
            departure_iata_code = flight_data.origin_airport
            arrival_city_name = flight_data.destination_city
            arrival_iata_code = flight_data.destination_airport
            outbound_date = flight_data.out_date
            inbound_date = flight_data.return_date
            stop_overs = flight_data.stop_overs
            via_city = flight_data.via_city
            notification_manager.send_notification(price, departure_city_name, departure_iata_code,arrival_city_name,arrival_iata_code, outbound_date, inbound_date,stop_overs,via_city)
