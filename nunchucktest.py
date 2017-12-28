#!/usr/bin/env python

import cwiid
import time
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
GPIO.setup(24, GPIO.OUT)  #LED to GPIO24


LED_1_AND_4_ON = 9
OFFSET = 5


def pressed(button_state, button_code):
	return button_state & button_code == button_code


def led(on_off):
    """Turn led <on_off>"""
    signal = on_off and GPIO.HIGH or GPIO.LOW
    GPIO.output(24, signal)
    print("LED ", on_off)


def rumble(wiimote):
    wiimote.rumble = 1
    time.sleep(0.5)
    wiimote.rumble = 0


def wiimote_msg_callback(msg_list, msg_time):
    print("Received", len(msg_list), "messages at time", msg_time, "...")
    for msg in msg_list:
        print(msg)
    print("")


def main():
    print('Press button 1 + 2 on your Wii Remote...')
    wm=cwiid.Wiimote()
    wm.rpt_mode = cwiid.RPT_NUNCHUK | cwiid.RPT_BTN
    wm.led = LED_1_AND_4_ON
    wm.mesg_callback = wiimote_msg_callback
    wm.enable(cwiid.FLAG_MESG_IFC)

    print('Wii Remote connected...')
    print('\nPress the HOME button to disconnect the Wii and end the application')
    rumble(wm)

    time.sleep(0.5)
    print wm.state

    active = True
    nunchuk_initial_position = wm.state['nunchuk']['stick']
    while active:
        stick = wm.state['nunchuk']['stick']
        x, y = [stick[i] - nunchuk_initial_position[i] for i in range(2)]
        if abs(x) > OFFSET or abs(y) > OFFSET:
          print x, y

        btns = wm.state['buttons']
        if pressed(btns, cwiid.BTN_HOME):
            active = False

        if pressed(btns, cwiid.BTN_PLUS):
            led(True)

        if pressed(btns, cwiid.BTN_MINUS):
            led(False)
	
    print("Bye")
    rumble(wm)
    led(False)
    wm.close()


if __name__ == "__main__":
    main()
