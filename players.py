from machine import Pin


# An array of player pin ex array pos 0 -> player 1 -> pin 13
PLAYERS_LED_PIN = [13, 12, 14, 27]
PLAYERS_BUZZER_PIN = [16, 17, 5, 18]
# PLAYERS_BUZZER_LED_PIN = [5, 17, 16, 4]
# Reset on 34
RESET = Pin(34, Pin.IN, Pin.PULL_UP)

PLAYERS_COUNT = len(PLAYERS_LED_PIN)

# leds
players_led = [Pin(i, Pin.OUT, value=1) for i in PLAYERS_LED_PIN]
players_buzzer = [Pin(i, Pin.IN, Pin.PULL_UP) for i in PLAYERS_BUZZER_PIN]
# inputs
players_state = [0]*PLAYERS_COUNT
# players_buzzer_led = [Pin(i, Pin.OUT, value=1) for i in PLAYERS_BUZZER_LED_PIN]
triggered = False


def reset_lights():
    for i in players_led:
        i.value(1)


def light_player(pos: int):
    "Turn on the led of a player"
    player_led = players_led[pos]
    player_led.value(0)

