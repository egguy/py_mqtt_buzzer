# Push my button

Doc sur le jeu où il faut slapper le plus rapidement possible un bouton

## Principe

$x joueur s'affrontent et doivent appuyer sur un bouton le plus vite possible

Suite à un appui, allumage du premier bouton appuyé, verrouillage des autres.

Quand un bouton est appuyé une variable globale empeche les autres boutons de se déclancher et le buzzer correspondant s'allume. L'envoi d'un reset (ou appui sur le reset), remet à 0 la variable, et coupe les lumiéres.

Le verrouillage d'un bouton individuel est permanent jusqu'a l'envoi d'un deverouillage. L'allumage du buzzer par MQTT est independant de son état.

Envoi des events en MQTT

## composants:

* Un ESP32 en micropython
* $x joueur
* $x input (boutons)
* $x out (pupitre)
* $x out pour boutons

# Mapping

```python
# An array of player led pin ex array pos 0 -> player 1 -> pin 13
PLAYERS_LED_PIN = [13, 12, 14, 27]
# input
PLAYERS_BUZZER_PIN = [25, 33, 32, 35]
# buzzer lights
PLAYERS_BUZZER_LED_PIN = [5, 17, 16, 4]
# Reset on 34
```

# Install

Download micropython ESP32 v 1.13 min
Upload on the board with esptools

upload on the board:
* primitives/
* config.py
* mqtt_as.py
* players.py
* main.py
* config.json

## config.json file

```json
{
  "server": "<server_ip_dns>",
  "ssid": "<wifi_ssid>",
  "wifi_pw": "<wifi_pass>",
  "user": "<mqtt_user>",
  "password": "<mqtt_password>"
}
```

# Protocol

Use MQTT protocol and broker

## topics + messages

* buzz/ping
  * every 10s send serial
* buzz/{serial}/events -> events sent by the buzzer controller
  * 0 -> 3: buzzer number pressed
  * r: reset pressed
* buzz/{serial}/config -> send config to the buzzer
  * reset -> reset the buzzer (all light off, allow a new press)
  * on $i -> set player $i buzzer light on
  * off $i -> turn of player $i led
  * lock -> prevent press
  * lock $i -> prevent player press (disable buzzer, don't touch light)
  * unlock -> unlock
  * unlock $i -> unlock as player (don't touch the light)
