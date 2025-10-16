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

# Timer pour clignotement LED
timer = Timer(-1)

# --- Variables globales ---
last_check_time = ticks_ms()
current_blink_freq = 0           
alarm_active = False

# --- Fonction de clignotement LED ---
def toggle_led(timer):
    led.toggle()
    print("toggle led")

def set_led_blink(freq):

    global timer, current_blink_freq
    if freq == current_blink_freq:
        return  # rien à faire si la frequence precedente est la meme que celle a placer
    timer.deinit()
    current_blink_freq = freq
    if freq > 0:
        timer.init(freq=freq, mode=Timer.PERIODIC, callback=toggle_led)
    else:
        led.off()

# --- cleanup pour la led et le buzzer ---
def cleanup():
    led.off()
    print("LED éteinte proprement")
    buzzer.duty_u16(0)
    print("BUZZER éteinte proprement")
    sys.exit(0)



def main():
    try:
        global last_check_time, alarm_active

        while True:

            now = ticks_ms() #déffini now comme le moment ou la boucle démare

            val = pot.read_u16()              
            val = int(val / 3265.75)+15#definie val comme in intervvale entre 15 et 35
            if ticks_diff(now, last_check_time) >= 1000:
                measurements = dht20.measurements
                last_check_time = now
                d.clear()
                d.setCursor(0,0)
                d.print(f"Ambient: {measurements['t']:.0f} °C")
                d.setCursor(0,1)
                d.print(f"set : {val}°C")

                diff = measurements['t']-val

                

                if diff > 3:
                    # Température > consigne +3°C 
                    d.setCursor(10, 0)
                    d.print("ALARM")
                    set_led_blink(2)  # LED à 2 Hz
                    buzzer.freq(1318)
                    buzzer.duty_u16(30000)
                    alarm_active = True

                elif diff > 0:
                    print(diff)
                    # Température > consigne 

                    set_led_blink(0.5)
                    buzzer.duty_u16(0)
                    alarm_active = False

                else:
                    # Température normale                
                    set_led_blink(0)
                    buzzer.duty_u16(0)
                    alarm_active = False
                        
            sleep(0.1)
    except:
        cleanup()
        raise

if __name__ == '__main__':
    main()

