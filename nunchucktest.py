
#!/usr/bin/env python

import cwiid
import time


LED_1_AND_4_ON = 9
OFFSET = 5


def pressed(button_state, button_code):
	return button_state & button_code == button_code


def led(on_off):
    """Turn led <on_off>"""
    print("LED ", on_off)


def main():
    print('Press button 1 + 2 on your Wii Remote...')
    wm=cwiid.Wiimote()
    wm.led = LED_1_AND_4_ON
    print('Wii Remote connected...')
    print('\nPress the HOME button to disconnect the Wii and end the application')

    wm.rpt_mode = cwiid.RPT_NUNCHUK | cwiid.RPT_BTN time.sleep(0.5)
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
            wm.close()
            active = False

        if pressed(btns, cwiid.BTN_PLUS):
            led(True)

        if pressed(btns, cwiid.BTN_MINUS):
            led(False)
	
    print("Bye")


if __name__ == "__main__":
    main()
