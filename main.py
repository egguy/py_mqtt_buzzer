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
locked = False
# queue to push message to mqtt
notification_queue = Queue(maxsize=16)
# Reset pin
reset_pin = Pin(19, Pin.IN, Pin.PULL_UP)


def button_press(pos: int) -> None:
    """
    Handler for button press
    """
    global locked  # Prevent creating local variable
    if locked:
        print("locked no press")
        return
    if players_lock[pos]:
        print("Player lock")
        return
    # Lock button press
    locked = True
    # light matching player
    light_player(pos)
    # Push player number in mqtt
    notification_queue.put_nowait(pos)


def reset_state():
    """
    Reset the buttons light and allow another press
    """
    global locked  # Prevent creating local variable
    locked = False
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


def receive_callback(topic: bytes, msg: bytes, retained):
    global locked
    print((topic, msg, retained))
    if msg == b'reset':
        reset_state()
    elif msg.startswith(b'on') and len(msg) == 4:
        player = msg[3] - 48  # 48 = char '0'
        if 0 <= player < len(players_led):
            print("light ", player)
            light_player(player)
    elif msg.startswith(b'off') and len(msg) == 5:
        player = msg[4] - 48  # 48 = char '0'
        if 0 <= player < len(players_led):
            print("off", player)
            lightoff_player(player)
    elif msg.startswith(b'lock'):
        if len(msg) == 4:
            print("lock")
            locked = True
        elif len(msg) == 6:
            player = msg[5] - 48
            if 0 <= player < len(players_led):
                print("plock", player)
                players_lock[player] = 1
    elif msg.startswith(b'unlock'):
        if len(msg) == 6:
            print("unlock")
            locked = False
        elif len(msg) == 8:
            player = msg[7] - 48
            if 0 <= player < len(players_led):
                print("punlock", player)
                players_lock[player] = 0


async def conn_han(mqtt_client):
    global ping
    await client.subscribe(config_topic)
    if not ping:
        asyncio.create_task(ping_task(mqtt_client))


async def ping_task(mqtt_client):
    global ping
    ping = True
    while True:
        await mqtt_client.publish(announce_topic, serial, qos=1)
        await asyncio.sleep(10)


async def main(mqtt_client, queue: Queue):
    await mqtt_client.connect()

    while True:
        data = await queue.get()
        print('publish', data)
        # If WiFi is down the following will pause for the duration.
        await mqtt_client.publish('buzz/{}/events'.format(serial), '{}'.format(data), qos=1)


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
