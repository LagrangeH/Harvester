#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.display import Display
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor, GyroSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4

from time import sleep


drive = MoveTank(OUTPUT_A, OUTPUT_B)
motor = LargeMotor(OUTPUT_C)
color_left, color_right, color_center = ColorSensor(INPUT_2), ColorSensor(INPUT_3), ColorSensor(INPUT_4)
infrared = InfraredSensor(INPUT_1)
led = Leds()
sound = Sound()
display = Display()

if __name__ == '__main__':
    led.animate_flash('GREEN')
    # sound.speak('hello')
