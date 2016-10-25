import forecastio
import datetime

from twilio.rest import TwilioRestClient
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

account_sid = parser.get('twilioKey', 'account_sid')
auth_token = parser.get('twilioKey', 'auth_token')

def main():
    api_key = parser.get('forecastioKey', 'api_key')

    lat = 38.554609
    lng = -121.753235
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrowEdit = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 10, 0, 0)
    print tomorrowEdit
    forecast = forecastio.load_forecast(api_key, lat, lng, time = tomorrowEdit)

    tomorrowForcast = forecast.hourly().icon
    if (tomorrowForcast == "rain"):
        sendText()

def sendText():

    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body="Bring your bike inside!",
        to="+16313381186",    # Replace with your phone number
        from_="+16319047251") # Replace with your Twilio number

    print(message.sid)

main()
