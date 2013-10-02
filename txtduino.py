import settings
import sys

from BreakfastSerial import Led, Arduino, Button
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

board = Arduino()
LED_PIN = 13
BUTTON_PIN = 2

led = Led(board, LED_PIN)
button = Button(board, BUTTON_PIN)

msg_sent = False

def down_press():
  global msg_sent
  print "button down"

  if not msg_sent:

      # Turn on the LED to indicate we are sending the txt message!
      led.on()
      try:
          client = TwilioRestClient(settings.twilio_account_sid,
                                settings.twilio_auth_token)
          message = client.sms.messages.create(
              body="Hello from Julia's rad Arduino!",
              to=settings.your_phone_number,
              from_=settings.your_twilio_number)

      except TwilioRestException as e:
          print "Ruh-roh got an error: %s" % e
          led.off()
          sys.exit(0)

      print "Attempting to send message, status is: %s" % message.status
      msg_sent = True
      led.off()

def up_press():
  print "button up"

button.down(down_press)
button.up(up_press)

while(not msg_sent):
    continue
