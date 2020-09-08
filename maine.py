import uasyncio as asyncio
from primitives.queue import Queue
from primitives.pushbutton import Pushbutton
from players import *


pressed = False
notification_queue = Queue(maxsize=16)
reset_pin = Pin(19, Pin.IN, Pin.PULL_UP)

def callback(topic, msg, retained):
    print((topic, msg, retained))


async def conn_han(client):
    await client.subscribe('foo_topic', 1)


async def main(client, queue: Queue):
    await client.connect()
    while True:
        data = await queue.get()
        print('publish', data)
        # If WiFi is down the following will pause for the duration.
        await client.publish('result', '{}'.format(data), qos = 1)

def button_press(pos):
    global pressed
    if pressed:
        print("Can't press agin")
        return
    print("Pressed")
    pressed = True
    light_player(pos)
    notification_queue.put_nowait(pos)


def reset():
    global pressed
    print("reseting")
    pressed = False
    notification_queue.put_nowait("reset")

pb_reset = Pushbutton(reset_pin)
pb_reset.press_func(reset)

for i, button in enumerate(players_buzzer):
    print(i, button)
    pb = Pushbutton(button, suppress=True)
    print(pb.rawstate())
    pb.press_func(button_press, (i,))


from mqtt_as import MQTTClient
from config import config

config['subs_cb'] = callback
config['connect_coro'] = conn_han

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
# loop = asyncio.get_event_loop()

try:
    asyncio.run(main(client, notification_queue))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors