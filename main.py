#!/usr/bin/env python3
# Documentation: https://python-ev3dev.readthedocs.io/en/latest/
from ev3dev2.motor import MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.display import Display
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor, GyroSensor, LightSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4, Sensor

from time import sleep
# from loguru import logger


wheels = MoveTank(OUTPUT_A, OUTPUT_B)
motor = MediumMotor(OUTPUT_C)
color_left, color_right = ColorSensor(INPUT_2), ColorSensor(INPUT_3)
color_center = ColorSensor(INPUT_4)
infrared = InfraredSensor(INPUT_1)
led = Leds()
sound = Sound()
display = Display()

BLACK = 1
WHITE = 6

SEED = 0
TREE = 1
NOTHING = 2

SPEED = 50
ROTATE_SPEED = SPEED - 40
MOTOR_ROTATE = 0.5 # TODO: change it

road_map = []


def forward():
    while True:
        if color_left.color() == WHITE:
            if color_right.color() == WHITE:
                wheels.on_for_rotations(SpeedPercent(SPEED), SpeedPercent(SPEED), 0.1)
            elif color_right.color() == BLACK:
                wheels.on_for_rotations(SpeedPercent(SPEED), SpeedPercent(ROTATE_SPEED), 0.1)
        elif color_left.color() == BLACK:
            if color_right.color() == WHITE:
                wheels.on_for_rotations(SpeedPercent(ROTATE_SPEED), SpeedPercent(SPEED), 0.1)
            elif color_right.color() == BLACK:
                wheels.stop_action('coast')
                break
    return True


def left():
    forward()
    return rotate_in_place('l')


def right():
    forward()
    return rotate_in_place('r')

   
def rotate_in_place(direction):
    direction = 1 if direction == 'r' else -1
    if direction not in (-1, 1):
        raise ValueError("Argument 'direction' must be 'r' or 'l'")
    return wheels.on_for_rotations(SpeedPercent(SPEED*direction), SpeedPercent(-SPEED*direction), 0.5)


def check_cell():
    try:
        if infrared.proximity() > 50:    # change this
            return False
        else:
            return True
    except Exception:
        return False


def check_item():
    if color_center.reflected_light_intensity() > 50:   # change this
        return SEED
    else:
        return TREE


def turn_over():
    return wheels.on_for_rotations(SpeedPercent(-SPEED), SpeedPercent(SPEED), 1)


def crossing():
    return wheels.on_for_rotations(SpeedPercent(SPEED), SpeedPercent(SPEED), 0.3)


def transfer_tree(step):
    take_item()
    turn_over()
    if not step % 2:
        left()
    else:
        right()
    forward()
    release_item()
    turn_over()

    if step == 1:
        left()
    else:
        forward()
        crossing()
        if step == 3:
            left()
        elif step in (4, 5):
            forward()
            crossing()
            if step == 5:
                left()
    return True


def take_item():
    wheels.on_for_rotations(SpeedPercent(100), SpeedPercent(100), 0,5, brake=False)
    motor.on_for_rotations(SpeedPercent(100), MOTOR_ROTATE)


def release_item():
    motor.on_for_rotations(SpeedPercent(100), -MOTOR_ROTATE)
    wheels.on_for_rotations(SpeedPercent(100), SpeedPercent(100), 0,5, brake=False)


def run():
    crossing()
    for step in range(6):

        if not step % 2: # step equal or 0, or 2, or 4
            right()

        if check_cell:
            forward()
            item = check_item()
            road_map.append(item)
            
            if item == SEED:
                turn_over()
                if not step % 2:
                    forward()
                    crossing()
                elif step == 5:
                    right()
                    forward()
                    crossing()
                    forward()
                    crossing()
                    forward()
                    # finish
                else:
                    left()
                # continue
            else:   # item == TREE

                transfer_tree(step)
                # continue
        else:
            road_map.append(NOTHING)
            if not step % 2:
                turn_over()
            else:
                rotate_in_place(right)
            # continue


if __name__ == '__main__':
    # run()

    # led.animate_flash('RED')
    sound.speak('Okey')
    # led.animate_flash('GREEN')
    # wheels.on_for_rotations(SpeedPercent(75), SpeedPercent(75), 5)
