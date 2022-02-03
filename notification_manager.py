from datetime import date
import requests
import smtplib

SHEETY_ENDPOINT = "<your endpoint>"
SHEETY_API = "<you api>"

sheety_header = {
    "Authorization": f"Bearer {SHEETY_API}"
}

class NotificationManager:


    def __init__(self,email,password,):
        self.users_data = {}
        self.email = email
        self.password = password
        self.get_data()


    def get_data(self):
        r = requests.get(url=SHEETY_ENDPOINT,headers=sheety_header)
        data = r.json()['users']
        self.users_data = data


    def send_notification(self,price,departure_city_name,departure_iata_code,arrival_city_name,arrival_iata_code,outbound_date,inbound_date,*args):

        message = f"low price alert! Only £{price} to fly from {departure_city_name}-{departure_iata_code} to {arrival_city_name}-{arrival_iata_code},from {outbound_date} to {inbound_date}"

        link = f"https://www.google.co.uk/flights?hl=en#flt={departure_iata_code}.{arrival_iata_code}.{outbound_date}*{arrival_iata_code}.{departure_iata_code}.{inbound_date}"

        if args[0] > 0:
            message = f"{message}\nFlight has {args[0]} stop over, via {args[1]}"
            
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(self.email,self.password)
                for user in self.users_data:
                    connection.sendmail(
                        from_addr=self.email,
                        to_addrs=user['email'],
                        msg=f"Subject:New Low Price Flight!\n\n{message}\n{link}".encode('utf-8')
                    )

        

