import forecastio
import datetime

from twilio.rest import TwilioRestClient
from ConfigParser import SafeConfigParser

#TODO: Make automatic everyday

#parse and initialize API keys
parser = SafeConfigParser()
parser.read('config.ini')

account_sid = parser.get('twilioKey', 'account_sid')
auth_token = parser.get('twilioKey', 'auth_token')

def main():
    api_key = parser.get('forecastioKey', 'api_key')

    #Lat and longitude for Davis, California
    lat = 38.554609
    lng = -121.753235

    #Gets tomorrows date
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    #Tomorrows date without milliseconds (for twilio)
    tomorrowEdit = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 10, 0, 0)

    #loads forcast for tomorrow
    forecast = forecastio.load_forecast(api_key, lat, lng, time = tomorrowEdit)
    tomorrowForcast = forecast.hourly().icon

    #Sends text if it will rain
    if (tomorrowForcast == "rain"):
        sendText()

def sendText():

    client = TwilioRestClient(account_sid, auth_token)
    myNumber = parser.get('PhoneNumbers', 'myNumber')
    twilioNumber = parser.get('PhoneNumbers', 'twilioNumber')

    message = client.messages.create(body="Bring your bike inside!",
        to= myNumber,
        from_= twilioNumber)

    print("Success, Sending text!")
    print ("Message ID:"  + message.sid)

main()
