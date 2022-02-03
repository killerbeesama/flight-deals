import requests

SHEETY_ENDPOINT = "<you endpoint>"
SHEETY_API = "<your api key>"

sheety_header = {
    "Authorization": f"Bearer {SHEETY_API}"
}

print("Welcome we find the best flight for you for cheap\nTo get started--")
name = input("Enter your first Name:\n")
l_name = input("Enter your Last Name:\n")
sign_up = False
while not sign_up:
    email = input("Enter your email:\n")
    ck_email = input("Enter your email again:\n")
    if email == ck_email:
        sheety_parameter = {
            "user": {
                "firstName": name,
                "lastName": l_name,
                "email": email,
            }
        }
        r = requests.post(url=SHEETY_ENDPOINT,
                          headers=sheety_header, json=sheety_parameter)
        print("Success")
        sign_up = True
    else:
        print("Check your email and try again")
