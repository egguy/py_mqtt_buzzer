import uasyncio as asyncio
from primitives.queue import Queue
from primitives.pushbutton import Pushbutton
from players import *

pressed = False
# queue to push message to mqtt
notification_queue = Queue(maxsize=16)
# Reset pin
reset_pin = Pin(19, Pin.IN, Pin.PULL_UP)


def button_press(pos: int) -> None:
    """
    Handler for button press
    """
    global pressed  # Prevent creating local variable
    if pressed:
        return
    # Lock button press
    pressed = True
    # light matching player
    light_player(pos)
    # Push player number in mqtt
    notification_queue.put_nowait(pos)


def reset():
    """
    Reset the buttons light and allow another press
    """
    global pressed  # Prevent creating local variable
    pressed = False
    reset_lights()
    # send reset message
    notification_queue.put_nowait("reset")


pb_reset = Pushbutton(reset_pin)
pb_reset.press_func(reset)

# Instanciate and attach button to the asyncio button manager
for i, button in enumerate(players_buzzer):
    pb = Pushbutton(button, suppress=True)
    pb.press_func(button_press, (i,))

# MQTT Section
# Need to import after button to prevent problem with asyncio loop handling
from mqtt_as import MQTTClient
from config import config


def receive_callback(topic, msg, retained):
    print((topic, msg, retained))


async def conn_han(client):
    await client.subscribe('foo_topic', 1)


async def main(client, queue: Queue):
    await client.connect()
    while True:
        data = await queue.get()
        print('publish', data)
        # If WiFi is down the following will pause for the duration.
        await client.publish('result', '{}'.format(data), qos=1)


config['subs_cb'] = receive_callback
config['connect_coro'] = conn_han

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
# loop = asyncio.get_event_loop()

try:
    asyncio.run(main(client, notification_queue))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
