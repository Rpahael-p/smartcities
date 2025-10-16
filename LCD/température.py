from lcd1602 import LCD1602
from dht20 import DHT20
from machine import I2C,Pin,ADC,PWM,Timer
from utime import sleep,ticks_ms, ticks_diff
import time
import sys

# --- Initialisation des périphériques ---
# LCD sur bus I2C1
i2c1 = I2C(1)#LCD
d = LCD1602(i2c1, 2, 16)
d.display()

# DHT20 sur bus I2C0
i2c0_sda = Pin(8)
i2c0_scl = Pin(9)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)
dht20 = DHT20(0x38, i2c0)

# Potentiomètre sur GPIO26
pot = ADC(Pin(26))           

# LED et Buzzer
led = Pin(18, Pin.OUT)
buzzer = PWM(Pin(27))   # Exemple : buzzer sur GPIO15

# Timer pour clignotement LED et LCD
timer = Timer(-1)
timerLCD = Timer(-1)
timerBuzzer = Timer(-1)

# --- Variables globales ---
last_check_time = ticks_ms()
current_blink_freq = 0           
buzzer_state = False
curentperiode= 1337

# --- Fonctions de clignotements ---
def toggle_led(timer):
    led.toggle()
    print("toggle led")


def LCDAllarm(timer):
    print("toggle alarm")
    d.clear()
    d.setCursor(0,0)
    d.print("ALARME")
    d.setCursor(0,1)
    d.print("ALARME")

def BuzzerAllarm(timer):
    global buzzer_state
    if buzzer_state:
        buzzer.freq(1337)
    else:
        buzzer.freq(2000)
    buzzer_state = not buzzer_state
    buzzer.duty_u16(30000)

def set_led_blink(freq):
    global timer, current_blink_freq
    '''
    il verifie que la frequence à changé. Si timer.deinit() est appler a chaque boucle
    si celui à 0.5 Hz est deinisialiser avant d'avoir le temps de clignoté une fois.
    ensuite il lance un timer qui inversera le status de la LED a la frequence fournie.
    '''

    if freq == current_blink_freq:
        return  # rien à faire si la frequence precedente est la meme que celle a placer
    timer.deinit()
    current_blink_freq = freq
    if freq > 0:
        timer.init(freq=freq, mode=Timer.PERIODIC, callback=toggle_led)
    else:
        led.off()

def set_allarm_blink():
    '''
    lance un timer qui se lancera une seul fois après 0.5 sec et affiche
    allarme sur le LCD comme les valeur de température sont afficher dans le code
    il alterne entre les deux.
    la premiere moitier de seconde avec les valeurs et la deuxieme
    avec allarme.
    '''
    timerLCD.deinit()
    
    timerLCD.init(mode=Timer.ONE_SHOT, period=500 , callback=LCDAllarm)

def set_buzzer_blink(i=2):
    """
    Fait alterner le buzzer entre 1337Hz et 2000Hz 'i' fois par seconde.
    i = 3 => changement 3x/s (toutes les ~0.33s)
    lorque la fonction est appeller, une fois par seconde,
    il lance un timer periodique qui alterné entre les deux fréquence
    le defaut est que lorce que i est impaire la derniere et la premiere fréquence
    sera 1337 Hz. La solution serait de varriable globale mais j'ai jugé ça
    un peux lourd pour pas grand chose.
    """
    global timerBuzzer
    timerBuzzer.deinit()
    period_ms = int(500 / i)  # demi-période : car deux changements pour un cycle complet
    timerBuzzer.init(mode=Timer.PERIODIC, period=period_ms, callback=BuzzerAllarm)


# --- cleanup pour la led, le LCD et le buzzer ---
'''
cleanup vas ici etre appeller par exepte et vas donc gérer toute les exeptions
mais sont but principale est de tout etteindre lorsque on arrete le programe.
'''
def cleanup():
    led.off()
    print("LED éteinte proprement")
    buzzer.duty_u16(0)
    print("BUZZER éteinte proprement")
    d.clear()
    print("BUZZER éteinte proprement")
    sys.exit(0)


'''
la boucle fonctionne en trois temps:
1)Now est definie et les valeur du multimetre sont lue.
2)Toute les secondes, les valeur du capteur sont lue et affiché sur le LCD
avec celle du multimetre
3)La difference entre la valeur mesuré et celle qui est voule est calculé 
et les if decide de ce qui sallume ou pas.
'''
def main():
    try:
        global last_check_time

        while True:

            now = ticks_ms() #déffini now comme le moment ou la boucle démare

            val = pot.read_u16()              
            val = int(val / 3265.75)+15#definie val comme in intervvale entre 15 et 35
            if ticks_diff(now, last_check_time) >= 1000:
                measurements = dht20.measurements
                last_check_time = now
                d.clear()
                d.setCursor(0,0)
                d.print(f"Ambient: {measurements['t']:.1f} °C")
                d.setCursor(0,1)
                d.print(f"set : {val}°C")

                diff = measurements['t']-val

                

                if diff > 3:
                    # Température > consigne +3°C
                    set_allarm_blink()
                    set_led_blink(2)  # LED à 2 Hz
                    set_buzzer_blink()

                elif diff > 0:
                    print(diff)
                    # Température > consigne 

                    set_led_blink(0.5) # LED à 0.5 Hz
                    buzzer.duty_u16(0)
                    timerBuzzer.deinit()

                else:
                    # Température normale                
                    set_led_blink(0) # LED eteinte
                    buzzer.duty_u16(0)
                    timerBuzzer.deinit()
                        
            sleep(0.1)
    except:
        cleanup()
        raise

if __name__ == '__main__':
    main()

