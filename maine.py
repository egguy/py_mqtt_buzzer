import uasyncio as asyncio
from primitives.queue import Queue
from primitives.pushbutton import Pushbutton
from players import *
from config import config, serial
# MQTT Section
from mqtt_as import MQTTClient

# game mode
NORMAL = const(1)
VERSUS = const(2)

config_topic = "buzz/{}/config".format(serial)
event_topic = "buzz/{}/events".format(serial)
announce_topic = "buzz/ping"

ping = False
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


def reset_state():
    """
    Reset the buttons light and allow another press
    """
    global pressed  # Prevent creating local variable
    pressed = False
    reset_lights()


def reset():
    reset_state()
    # send reset message
    notification_queue.put_nowait("r")


pb_reset = Pushbutton(reset_pin)
pb_reset.press_func(reset)

# Instanciate and attach button to the asyncio button manager
for i, button in enumerate(players_buzzer):
    pb = Pushbutton(button, suppress=True)
    pb.press_func(button_press, (i,))


def receive_callback(topic, msg, retained):
    print((topic, msg, retained))
    if msg == b'reset':
        reset_state()


async def conn_han(client):
    global ping
    await client.subscribe(config_topic)
    if not ping:
        asyncio.create_task(ping_task(client))


async def ping_task(client):
    global ping
    ping = True
    while True:
        await client.publish(announce_topic, serial, qos=1)
        await asyncio.sleep(10)


async def main(client, queue: Queue):
    await client.connect()

    while True:
        data = await queue.get()
        print('publish', data)
        # If WiFi is down the following will pause for the duration.
        await client.publish('buzz/{}/events'.format(serial), '{}'.format(data), qos=1)


config['subs_cb'] = receive_callback
config['connect_coro'] = conn_han

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
# loop = asyncio.get_event_loop()

print("Serial: {}".format(serial))

try:
    asyncio.run(main(client, notification_queue))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
