import sys
import time

from Adafruit_IO import *

ADAFRUIT_IO_KEY      = '77984bef8d584acc842e0e4cc50480c4'
ADAFRUIT_IO_USERNAME = 'pfrench'

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'climate-data-1'
FEED_ID2 = 'climate-data-2'
FEED_ID3 = 'climate-data-3'
FEED_ID4 = 'climate-data-4'
FEED_ID_TEMP = 'temperature'
FEED_ID_HEATING = 'heating'
FEED_ID_COOLING = 'cooling'


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print 'Connected to Adafruit IO!  Listening for changes...'
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(FEED_ID)
    client.subscribe(FEED_ID2)
    client.subscribe(FEED_ID3)
    client.subscribe(FEED_ID4)
    client.subscribe(FEED_ID_TEMP)
    client.subscribe(FEED_ID_COOLING)
    client.subscribe(FEED_ID_HEATING)
	
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print 'Disconnected from Adafruit IO!'
    sys.exit(1)

count = 0
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
	if count == 4:
	    print 'Publishing current temperature to feedback.'
            client.publish('feedback', 'Current average temperature: ' + str(totalTemp / 4) + ' degrees F')
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