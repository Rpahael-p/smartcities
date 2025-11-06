from machine import Pin
from servo import SERVO
from time import sleep
import ntptime
import network
import time
import sys

def cleanup():
    servo.turn(0)
    sleep(1)
    sys.exit(0)

SSID = "electroProjectWifi"
PASSWORD = "B1MesureEnv"

nic = network.WLAN(network.STA_IF)
nic.active(True)

button_pin = Pin(16, Pin.IN, Pin.PULL_UP)

# --- Fonction appelée lors de l'appui ---
def on_button_pressed(pin):
    print("Bouton pressé !")

# --- Attacher l'interruption ---
button_pin.irq(trigger=Pin.IRQ_FALLING, handler=on_button_pressed)

if not nic.isconnected():
    print("Connexion au reseau Wi-Fi...")
    nic.connect(SSID, PASSWORD)
    t0 = time.time()
    while not nic.isconnected():
        if time.time() - t0 > 15:  # timeout 15 sec
            raise RuntimeError("Impossible de se connecter au Wi-Fi")
        time.sleep(1)

print("Connecté ! Adresse IP :", nic.ifconfig()[0])

servo = SERVO(Pin(20))

# Synchronisation NTP
ntptime.settime()

# Lecture de l'heure actuelle
current_time = time.localtime()[3]
print("Heure actuelle UTC :", current_time)

if(current_time>12):
    current_time=current_time-12

angle=(180/12)*current_time

try:
    print(angle)
    servo.turn(angle)

    sleep(1)

    servo.turn(0)

    sleep(1)

    servo.turn(180)

    sleep(1)
except:
    cleanup()
    raise