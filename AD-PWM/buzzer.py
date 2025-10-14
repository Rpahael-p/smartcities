from machine import Pin, ADC, PWM
from time import sleep

buzzer = PWM(Pin(27))        # buzzer sur GPIO27
led = Pin(18, Pin.OUT)       # LED sur GPIO18
pot = ADC(Pin(26))           # potentiomètre sur GPIO26
button = Pin(16, Pin.IN,Pin.PULL_DOWN)  # Bouton        
status = True
last_state = 0

#============handler=============

#A la recepton du signal le handler inverse status pour qu'à la prochaine boucle la musique change
def handle_interrupt(pin):
    global status
    status = not status

#=============Listener============

button.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)#il attend que le bouton soi relacher pur envoyer un signal


#=============volume==============
def get_volume():
    val = pot.read_u16()              
    val = int(val / 10)                # divise la plage pour silencer
    return val         
#=============note==============
def DO(time):
    buzzer.freq(1046)
    buzzer.duty_u16(get_volume())
    led.value(1)
    sleep(time/2)
    led.value(0)
    sleep(time/2)
    buzzer.duty_u16(0)

def RE(time):
    buzzer.freq(1175)
    buzzer.duty_u16(get_volume())
    led.value(1)
    sleep(time/2)
    led.value(0)
    sleep(time/2)
    buzzer.duty_u16(0)

def MI(time):
    buzzer.freq(1318)
    buzzer.duty_u16(get_volume())
    led.value(1)
    sleep(time/2)
    led.value(0)
    sleep(time/2)
    buzzer.duty_u16(0)

def FA(time):
    buzzer.freq(1397)
    buzzer.duty_u16(get_volume())
    led.value(1)
    sleep(time/2)
    led.value(0)
    sleep(time/2)
    buzzer.duty_u16(0)

def SO(time):
    buzzer.freq(1568)
    buzzer.duty_u16(get_volume())
    led.value(1)
    sleep(time/2)
    led.value(0)
    sleep(time/2)
    buzzer.duty_u16(0)

def LA(time):
    buzzer.freq(1760)
    buzzer.duty_u16(get_volume())
    led.value(1)
    sleep(time/2)
    led.value(0)
    sleep(time/2)
    buzzer.duty_u16(0)

def SI(time):
    buzzer.freq(1967)
    buzzer.duty_u16(get_volume())
    led.value(1)
    sleep(time/2)
    led.value(0)
    sleep(time/2)
    buzzer.duty_u16(0)

def N(time):
    buzzer.duty_u16(0)
    led.value(0)
    sleep(time)

#=============boucle principale==============
while True:

    if status==True: #Choix de la musique
        DO(0.25)
        RE(0.25)
        MI(0.25)
        DO(0.25)
        N(0.01)

        MI(0.25)
        FA(0.25)
        SO(0.5)

        MI(0.25)
        FA(0.25)
        SO(0.5)
        N(0.01)

        SO(0.125)
        LA(0.125)
        SO(0.125)
        FA(0.125)
        MI(0.25)
        DO(0.25)

        SO(0.125)
        LA(0.125)
        SO(0.125)
        FA(0.125)
        MI(0.25)
        DO(0.25)

        RE(0.25)
        SO(0.25)
        DO(0.5)
        N(0.01)

        RE(0.25)
        SO(0.25)
        DO(0.5)
    else:
        DO(0.25)
        N(0.01)
        DO(0.25)
        N(0.01)
        SO(0.25)
        N(0.01)
        SO(0.25)
        N(0.01)
        LA(0.25)
        N(0.01)
        LA(0.25)
        N(0.01)
        SO(0.5)
        N(0.01)
        
        FA(0.25)
        N(0.01)
        FA(0.25)
        N(0.01)
        MI(0.25)
        N(0.01)
        MI(0.25)
        N(0.01)
        
        RE(0.25)
        N(0.01)
        RE(0.25)
        N(0.01)
        DO(0.5)
        N(0.01)