from machine import Pin
import time

# Configuration des broches
led = Pin(18, Pin.OUT)        # LED sur 
button = Pin(16, Pin.IN)  # Bouton 

mode = 0  # 0 = éteint, 1 = lent, 2 = rapide
last_state = 1
last_press_time = 0

led_state = 0 #état de la led
last_toggle_time = time.ticks_ms() #derniere fois que la lampe a changé d'état

while True:
    now = time.ticks_ms() #déffini now comme le moment ou la boucle démare

    # --- Gestion du bouton ---
    current_state = button.value()
    if last_state == 1 and current_state == 0:  # si le bonton est appuyé sur cette boucle mais ne l'était pas la boucle précédente
        # anti-rebond : ignorer si <200 ms depuis le dernier appui
        # pour evité des resultat imprévu en cas d'appuis rapide sur le bouton
        if time.ticks_diff(now, last_press_time) > 200:
            mode = (mode + 1) % 9 # le 9 peut etre remplacé par trois si on veux que le mode change a chaque appuis en l'état il changera tout les 3 appuis.
            last_press_time = now 
    last_state = current_state

 

    # --- Gestion de la LED selon le mode ---
    # le principe est ici le même que pour le projet arroseur de l'anné passé.
    # le programe verifie le mode pour choisir dans quelle if rentrer pour ensuite verrifier que le temps est ecoulé et si oui changé l'état de la led.
    if mode in (0, 1, 2): #(0, 1, 2) peut etre modifier par silmplement 0 dans le cas ou l'onvoudrait que chaque appuis change le mode.
        led.value(0)  # garde la led éteinte.

    elif mode in (3, 4, 5): #(3, 4, 5) par 1
        # clignotement lent 0,5 Hz = période 2000 ms
        if time.ticks_diff(now, last_toggle_time) >= 2000:  # change toutes les 2s
            led_state = not led_state #le statut de la bool est simplement inversé
            led.value(led_state)
            last_toggle_time = now #deffini la dernier fois que la led a été modifier par maintenant

    elif mode in (6, 7, 8):#(6, 7, 8) par 2
        # clignotement rapide 2 Hz = période 500 ms
        if time.ticks_diff(now, last_toggle_time) >= 250:  # change toutes les 0,25s
            led_state = not led_state
            led.value(led_state)
            last_toggle_time = now

