from machine import Pin
from servo import SERVO
from time import sleep, time as ticks
import ntptime
import network
import time
import sys

#la fonction cleanup remet le servo au point mort avant de couper le programe.
def cleanup():
    servo.turn(0)
    sleep(1)
    sys.exit(0)

SSID = "electroProjectWifi"
PASSWORD = "B1MesureEnv"
fuseau=0
mode=12
last_button = 0  
double_click_max_delay = 0.2 
last_irq_time = 0

nic = network.WLAN(network.STA_IF)
nic.active(True)

button_pin = Pin(16, Pin.IN, Pin.PULL_UP)

# --- Gestion des appuis sur le bouton ---
def on_button_pressed(pin):
    global fuseau, mode, last_button, last_irq_time

    now = ticks()
    #filtre anti rebond qui verifie que la bouton na pas été 
    #pressé trop récament.
    if now - last_irq_time < 0.01:
        return
    last_irq_time = now

    # détection double appui
    #si le bouton est appuyer deux fois en 500ms le mode globale est echangé entre 12 et 24
    if time.ticks_diff(time.ticks_ms(), last_button) < 500:
        mode = 24 if mode == 12 else 12
        print(f"Double appui : mode changé -> {mode}h")
        last_press_time = 0  # réinitialiser pour ne pas refaire un triple clic
    else:
        #une varriable fuseau vas de 0 a 10 a chaque presion du bouton la varriable est incrémenté.
        fuseau += 1
        if fuseau == 11:
            fuseau = 0

        if fuseau <= 5:
            print(f"Fuseau changé à UTC +{fuseau}")
        else:
            print(f"Fuseau changé à UTC -{fuseau-5}")

    last_button = time.ticks_ms()
 

    change_heure()#comme dans les deux cas l'heure a afficher est changé on appale la fonction qui s'occupe de ca.


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

def change_heure():
    global fuseau, mode

    try:
        ntptime.settime() #on sincronise le temps interne avec celui du serveur ntp.
    except OSError:
        print("Erreur NTP : impossible de synchroniser l'heure")

    # Lecture de l'heure actuelle
    current_time = time.localtime()[3]

    current_time %= 24  # reste dans 0-23

    # Ajustement du fuseau
    #si <5 alors on ajoute si >5 on retire x-5
    if fuseau <= 5:
        current_time += fuseau
    else:
        current_time -= (fuseau - 5)

    current_time %= 24  # reste dans 0-23
        # Passage en mode 12h si nécessaire
    display_time = current_time
    if mode == 12:
        if display_time > 12:
            display_time -= 12

    angle = (180 / mode) * display_time
    print(f"Heure actuelle : {current_time} | Mode : {mode}h | Angle servo : {angle}")
    servo.turn(angle)

def main():
    try:
        # Synchronisation NTP
        ntptime.settime()

        change_heure()
        while 1:
            sleep(10)
            change_heure()# Le programe mets a jour l'heure toute les 10 seconde.
    except:
        cleanup()
        raise

if __name__ == '__main__':
    main()

