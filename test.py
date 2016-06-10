import sys
import time

from Adafruit_IO import *

ADAFRUIT_IO_KEY      = '...'
ADAFRUIT_IO_USERNAME = '...'

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = '...'

NUMBER_OF_SENSORS = 1

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print 'Connected to Adafruit IO!  Listening for changes...'
    # Subscribe to changes on FEED_ID.
    client.subscribe(FEED_ID)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print 'Disconnected from Adafruit IO!'
    sys.exit(1)

# Counts the number of feeds that have updated
count = 0

# Adds together the updated temperatures to be averaged later
totalTemp = 0.0

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.cli
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    global count
    global totalTemp

    print 'Feed {0} received new value: {1}'.format(feed_id, payload)
    if feed_id == FEED_ID_TEMP:
	    print 'Publishing temperature change to feedback.'
        client.publish('feedback', 'Registered temperature change of ' + payload + '.')
    if feed_id == FEED_ID or feed_id == FEED_ID2 or feed_id == FEED_ID3 or feed_id == FEED_ID4:
	       count += 1
	       totalTemp += float(payload)

    # Publishes to a feed called feedback that is an overall feed of what the system is doing
	if count == NUMBER_OF_SENSORS:
	    print 'Publishing current temperature to feedback.'
        client.publish('feedback', 'Current average temperature: ' + str(totalTemp / NUMBER_OF_SENSORS) + ' degrees F')
	    count = 0
	    totalTemp = 0.0

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

client.loop_blocking()
