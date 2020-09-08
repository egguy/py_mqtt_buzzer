# Push my button faster

Doc sur le jeu pour il faut slapper le plus rapidement un bouton

## Principe

$x joueur s'affrontent et doivent appuyer sur un bouton le plus vite possible

Suite à un appui, allumage du premier bouton appuyé, verrouillage des autres

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
