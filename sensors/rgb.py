from ws2812 import WS2812
from machine import ADC
from utime import sleep, ticks_ms
import urandom

# --- Couleurs ---
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

# --- Initialisation ---
SOUND_SENSOR = ADC(1)
led = WS2812(18, 1)

THRESHOLD = 2000
DECAY = 200
last_beat = 0

mesures = []
pic = []

# Variables pour le calcul des BPM
beat_times = []         # Liste des temps entre battements
bpm_list = []            # Liste des BPM récents
minute_start = ticks_ms()  # Temps du début de la minute


def moyenne(array):

    if len(array) == 0:
        return -1  # éviter division par zéro
    
    moyenne = sum(array) / len(array)
    return moyenne 

def prendre_mesure(array):
    """
    Lit le capteur de son et ajoute la valeur dans array.
    Si array a déjà 20 valeurs, supprime la plus ancienne.
    
    :param array: liste contenant les dernières mesures
    """
    # Lecture du capteur
    noise = SOUND_SENSOR.read_u16() / 256

    # Vérifier la taille de la liste
    if len(array) >= 20:
        array.pop(0)  # supprime la plus ancienne mesure

    array.append(noise)  # ajoute la nouvelle mesure

    return noise  # optionnel, renvoie la valeur mesurée

def prendre_pic(array,noise):
    """
    Lit le capteur de son et ajoute la valeur dans array.
    Si array a déjà 20 valeurs, supprime la plus ancienne.
    
    :param array: liste contenant les dernières mesures
    """
    # Vérifier la taille de la liste
    if len(array) >= 50:
        array.pop(0)  # supprime la plus ancienne mesure

    array.append(noise)  # ajoute la nouvelle mesure

    return noise  # optionnel, renvoie la valeur mesurée


while True:
    noise = prendre_mesure(mesures)
    now = ticks_ms()

    """
    Les pics son detecter en comparant une valeur avec les valeurs precendante.
    Si la valeur actuelle est 3 fois superieur a la moyenne des 20 valeurs précédente.
    De plus un pic ne peux pas etre trop proche du pic precedent il y à donc un decay.

    si un pic est detecter la lampe est allumer avec un couleur aleatoire dans une liste 
    sinon elle est éteinte.
    """

    # Détection de pics
    if noise > moyenne(mesures)*3 and (now - last_beat) > DECAY:
        print("pic detecter")

        # Calcul du BPM instantané
        if last_beat != 0:
            interval_ms = now - last_beat
            bpm = 60000 / interval_ms 
            bpm_list.append(bpm)
            beat_times.append(now)
            print("BPM instantané :", round(bpm, 2))

        last_beat = now

        # Choisir une couleur aléatoire
        color = urandom.choice(COLORS)

        # Afficher la couleur
        led.pixels_fill(color)
        led.pixels_show()
        prendre_pic(pic,noise)

    else:
        if (now - last_beat) > DECAY:
            led.pixels_fill((0, 0, 0))  # LED éteinte
            led.pixels_show()

    """
    Toute les minute le programe fais la moyenne du temps entre deux pic et ecris la réponse dans un a fichier texte.
    """
        # Vérifie si une minute est écoulée
    if (now - minute_start) >= 60000:  # 60 secondes
        bpm_moyen = moyenne(bpm_list)
        if bpm_moyen > 0:
            print("BPM moyen sur la dernière minute :", round(bpm_moyen, 2))

            # Écriture dans le fichier texte
            try:
                with open("bpm_log.txt", "a") as f:
                    f.write("BPM moyen: {:.2f}\n".format(bpm_moyen))
                print("BPM enregistré dans bpm_log.txt")
            except Exception as e:
                print("Erreur écriture fichier :", e)

        # Réinitialisation pour la minute suivante
        bpm_list = []
        minute_start = now

    # --- Envoi du niveau sonore sur le port série ---
    print(noise)

    sleep(0.01)

print("pic moyen",moyenne(pic))