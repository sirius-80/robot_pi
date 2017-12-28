#!/usr/bin/env python

import cwiid
import logging
import time
import traceback

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


class WiimoteControl(object):
    def __init__(self):
        self._connect()
        self.wiimote.rpt_mode = cwiid.RPT_NUNCHUK | cwiid.RPT_BTN
        self.wiimote.enable(cwiid.FLAG_MESG_IFC)
        self.wiimote.mesg_callback = self._wii_msg_callback
        nunchuk_initial_position = self.wiimote.state['nunchuk']['stick']

    def _connect(self):
        print('Press button 1 + 2 on your Wii Remote...')
        self.wiimote = None
        # while not wiimote:
        try:
            self.wiimote = cwiid.Wiimote()
        except:
            traceback.print_exc()
        print('Wii Remote connected...')
        print('\nPress the HOME button to disconnect the Wii and end the application')
        self.rumble()

    def _wii_msg_callback(self, mesg_list, time):
        for mesg in mesg_list:
            if mesg[0] == cwiid.MESG_BTN:
                if mesg[1] == cwiid.BTN_PLUS:
                    logging.info("LED on")
                    self.rumble()
                    led(True)
                if mesg[1] == cwiid.BTN_MINUS:
                    self.rumble()
                    led(False)
                    logging.info("LED of")
            if mesg[0] == cwiid.MESG_NUNCHUK:
                print(mesg[1])

    def rumble(self):
        self.wiimote.rumble = 1
        time.sleep(0.2)
        self.wiimote.rumble = 0

    def close(self):
        self.wiimote.close()


def main():
    controller = WiimoteControl()
    try:
        while True:
            time.sleep(1)
    finally:
        led(False)
        controller.close()


def main_old():
    wm.rpt_mode = cwiid.RPT_NUNCHUK | cwiid.RPT_BTN
    wm.led = LED_1_AND_4_ON
    wm.mesg_callback = wiimote_msg_callback

    print('Wii Remote connected...')
    print('\nPress the HOME button to disconnect the Wii and end the application')
    rumble(wm)

    time.sleep(0.5)
    print wm.state

    active = True
    nunchuk_initial_position = wm.state['nunchuk']['stick']
    while active:
        time.sleep(.1)
        # stick = wm.state['nunchuk']['stick']
        # x, y = [stick[i] - nunchuk_initial_position[i] for i in range(2)]
        # if abs(x) > OFFSET or abs(y) > OFFSET:
        #   print x, y
        #
        # btns = wm.state['buttons']
        # if pressed(btns, cwiid.BTN_HOME):
        #     active = False
        #
        # if pressed(btns, cwiid.BTN_PLUS):
        #     led(True)
        #
        # if pressed(btns, cwiid.BTN_MINUS):
        #     led(False)
	
    print("Bye")
    rumble(wm)
    led(False)
    wm.close()


if __name__ == "__main__":
    main()
