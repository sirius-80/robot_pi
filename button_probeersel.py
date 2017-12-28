import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
GPIO.setup(24, GPIO.OUT)  #LED to GPIO24


def lamp_aan():
    GPIO.output(24, True)


def lamp_uit():
    GPIO.output(24, False)

AAN = False
UIT = True

try:
    knop_toestand_oud = UIT
    knipper_stand = UIT
    teller = 0
    while True:
         knop_toestand_nieuw = GPIO.input(23)
         if knop_toestand_nieuw != knop_toestand_oud:
             if knop_toestand_nieuw == AAN:
                 teller = teller + 1
                 knipper_stand = not knipper_stand
                 print("Knop " + str(teller) + "X ingedrukt...")
             else:
                 lamp_uit()
                 print("Knop losgelaten...")
         knop_toestand_oud = knop_toestand_nieuw
         if knipper_stand == AAN:
             lamp_aan()
             time.sleep(0.1)
             lamp_uit()
             time.sleep(0.1)
         
except:
    GPIO.cleanup()
    print("Reset")
    raise
