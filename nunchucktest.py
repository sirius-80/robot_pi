#!/usr/bin/env python

import cwiid
import logging
import numpy
import RPi.GPIO as GPIO
import time
import concurrent.futures


class GpioController(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button to GPIO23
        GPIO.setup(24, GPIO.OUT)  # LED to GPIO24
        self.blinking = False
        self.executor = concurrent.futures.ThreadPoolExecutor(4)

    def led_blinking(self, on_off):
        self.blinking = on_off
        def do_blink():
            while self.blinking:
                self._led(True)
                time.sleep(.333333/2)
                self._led(False)
                time.sleep(.333333/2)
        if on_off:
            self.executor.submit(do_blink)

    def led(self, on_off):
        self.blinking = False
        self._led(on_off)

    def _led(self, on_off):
        """Turn led (connected to pin 24) <on_off>"""
        signal = on_off and GPIO.HIGH or GPIO.LOW
        GPIO.output(24, signal)
        logging.info("LED {}", on_off and "on" or "off")

    def close(self):
        self.led(False)
        GPIO.cleanup()


class WiimoteControl(object):
    def __init__(self):
        self.STICK_THRESHOLD = 1
        self.STICK_CENTER_POSITION = (127, 127)
        self.last_direction = (0, 0)
        self._connect()
        self.wiimote.rpt_mode = cwiid.RPT_NUNCHUK | cwiid.RPT_BTN
        self.wiimote.enable(cwiid.FLAG_MESG_IFC)
        self.wiimote.mesg_callback = self._wii_msg_callback
        self.wiimote.led = 9
        self.button_callback_functions = {}
        # Nunchuk needs some time to start reporting
        time.sleep(.2)

    def on_button(self, button, function, *args, **kwargs):
        self.button_callback_functions[button] = (function, args, kwargs)

    def _connect(self):
        print('Press button 1 + 2 on your Wii Remote...')
        self.wiimote = None
        self._connected = False
        while not self.wiimote:
            try:
                self.wiimote = cwiid.Wiimote()
                self._connected = True
                print('Wii Remote connected...')
                print('\nPress the HOME button to disconnect the Wii and end the application')
                self.rumble()
            except RuntimeError:
                logging.warn("Timed out waiting for wii-remote, trying again...")
            except KeyboardInterrupt:
                logging.warn("Interrupted. Stopping.")

    def _wii_msg_callback(self, mesg_list, time):
        for mesg in mesg_list:
            if mesg[0] == cwiid.MESG_BTN:
                button = mesg[1]
                if button in self.button_callback_functions:
                    func = self.button_callback_functions[button][0]
                    args = self.button_callback_functions[button][1]
                    kwargs = self.button_callback_functions[button][2]
                    func(*args, **kwargs)
            if mesg[0] == cwiid.MESG_NUNCHUK:
                # {'acc': (76, 127, 139), 'buttons': 0, 'stick': (126, 127)}
                stick = mesg[1]['stick']
                direction = numpy.subtract(stick, self.STICK_CENTER_POSITION)
                change = numpy.subtract(self.last_direction, direction)
                if abs(change[0]) >= self.STICK_THRESHOLD or abs(change[1]) >= self.STICK_THRESHOLD:
                    print("Direction", direction)
                self.last_direction = direction

    def connected(self):
        return self._connected

    def rumble(self, duration_seconds=0.1):
        self.wiimote.rumble = 1
        time.sleep(duration_seconds)
        self.wiimote.rumble = 0

    def close(self):
        if self._connected:
            self.rumble(0.5)
            self.wiimote.close()
        self._connected = False


def main():
    wii_controller = WiimoteControl()
    board_controller = GpioController()

    wii_controller.on_button(cwiid.BTN_HOME, wii_controller.close)
    wii_controller.on_button(cwiid.BTN_PLUS, board_controller.led, True)
    wii_controller.on_button(cwiid.BTN_MINUS, board_controller.led, False)
    wii_controller.on_button(cwiid.BTN_A, board_controller.led_blinking, True)
    wii_controller.on_button(cwiid.BTN_B, board_controller.led_blinking, False)

    try:
        while wii_controller.connected():
            time.sleep(.1)
    finally:
        board_controller.close()
        wii_controller.close()


if __name__ == "__main__":
    main()
