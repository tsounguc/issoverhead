
import requests
from datetime import datetime
import smtplib
import time
MY_LAT = 38.907192  # Your latitude
MY_LONG = -77.036873  # Your longitude
my_email = "tsounguc@mail.gvsu.edu"
password = "quzkqmfgwiklcqqz"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    print(data)

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    return MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    # If the ISS is close to my current position
    # and it is currently dark
    # Then send me an email to tell me to look up.
    # BONUS: run the code every 60 seconds.
    return time_now > sunset or time_now < sunrise

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            # Secure connection with Transport Layer Security
            connection.starttls()
            # Login to account
            connection.login(user=my_email, password=password)
            # Send email
            connection.sendmail(from_addr=my_email,
                                to_addrs=my_email,
                                msg=f"Subject:Look up\n\nThe ISS is above you in the sky")
