import forecastio
import datetime
import fbchat

###import and use twilio function for texting instead of messenger###

#from twilio.rest import TwilioRestClient

from ConfigParser import SafeConfigParser

#Parse config file
parser = SafeConfigParser()

#Change with your own directory
parser.read('/home/pi/Documents/GitHub/Raincheck/config.ini')


def main():
    #Get weather API key
    api_key = parser.get('forecastioKey', 'api_key')

    #Lat and longitude for Davis, California
    lat = 38.554609
    lng = -121.753235

    #Gets tomorrows date
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    #Tomorrows date without milliseconds (for twilio)
    twilioTomorrow = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 10, 0, 0)

    #loads forcast for tomorrow
    forecast = forecastio.load_forecast(api_key, lat, lng, time = twilioTomorrow)
    tomorrowForcast = forecast.hourly().icon

    #Sends text if it will rain
    if (tomorrowForcast == "rain"):
        message = "Bring your bike inside, it's going to rain tomorrow!"
        print(message)
        fbMessege(message)

    else:
        message = "It's not going to rain tomorrow, just want to wish you a great day"
        print(message)
        fbMessege(message)

        
#fb messenger is better
def fbMessege(message):
    username = parser.get('messenger', 'myUsername')
    password = parser.get('messenger', 'myPassword')
    UID = parser.get('messenger', 'myUID')

    client = fbchat.Client(username, password)

    sent = client.send(UID, message)

    if sent:
        print("Message sent successfully!")

#function for text if preferred
def sendText():

    #Get Twilio API keys
    account_sid = parser.get('twilioKey', 'account_sid')
    auth_token = parser.get('twilioKey', 'auth_token')

    client = TwilioRestClient(account_sid, auth_token)
    myNumber = parser.get('PhoneNumbers', 'myNumber')
    twilioNumber = parser.get('PhoneNumbers', 'twilioNumber')

    message = client.messages.create(body="Bring your bike inside, It's going to rain tomorrow!",
        to= myNumber,
        from_= twilioNumber)

    print("Success, Sending text!")
    print ("Message ID:"  + message.sid)

main()
