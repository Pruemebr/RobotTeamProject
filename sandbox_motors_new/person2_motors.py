"""
Functions for SPINNING the robot LEFT and RIGHT.
Authors: David Fisher, David Mutchler and Zikang Zhang.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

# DONE: 2. Implment spin_left_seconds, then the relevant part of the test function.
#          Test and correct as needed.
#   Then repeat for spin_left_by_time.
#   Then repeat for spin_left_by_encoders.
#   Then repeat for the spin_right functions.


import ev3dev.ev3 as ev3
import time


def test_spin_left_spin_right():
    """
    Tests the spin_left and spin_right functions, as follows:
      1. Repeatedly:
          -- Prompts for and gets input from the console for:
             -- Seconds to travel
                  -- If this is 0, BREAK out of the loop.
             -- Speed at which to travel (-100 to 100)
             -- Stop action ("brake", "coast" or "hold")
          -- Makes the robot run per the above.
      2. Same as #1, but gets degrees and runs spin_left_by_time.
      3. Same as #2, but runs spin_left_by_encoders.
      4. Same as #1, 2, 3, but tests the spin_right functions.
    """
#   spin_left_seconds:
    while True:
        print('Followings are for spin_left_seconds: ')
        turning_time = float(input('Enter the seconds to travel: '))
        if turning_time == 0:
            break
        speed = int(input('Enter the speed: '))
        stop_action = input('Enter the stop action: ')

        spin_left_seconds(turning_time, speed, stop_action)

#   spin_left_by_time:
    while True:
        print('Followings are for spin_left_by_time: ')
        degrees = int(input('Enter the turning angle: '))
        if degrees == 0:
            break
        speed = int(input('Enter the speed: '))
        stop_action = input('Enter the stop action: ')

        spin_left_by_time(degrees, speed, stop_action)

#   spin_left_by_encoders:
    while True:
        print('Followings are for spin_left_by_encoders: ')
        degrees = int(input('Enter the turning degrees: '))
        if degrees == 0:
            break
        speed = int(input('Enter the speed: '))
        stop_action = input('Enter the stop action: ')

        spin_left_seconds(degrees, speed, stop_action)

#   spin_right_seconds:
    while True:
        print('Followings are for spin_right_seconds: ')
        turning_time = float(input('Enter the seconds to travel: '))
        if turning_time == 0:
            break
        speed = int(input('Enter the speed: '))
        stop_action = input('Enter the stop action: ')

        spin_right_seconds(turning_time, speed, stop_action)

#   spin_right_by_time:
    while True:
        print('Followings are for spin_right_by_time: ')
        degrees = int(input('Enter the turning angle: '))
        if degrees == 0:
            break
        speed = int(input('Enter the speed: '))
        stop_action = input('Enter the stop action: ')

        spin_right_by_time(degrees, speed, stop_action)

#   spin_right_by_encoders:
    while True:
        print('Followings are for spin_right_by_encoders: ')
        degrees = int(input('Enter the turning angle: '))
        if degrees == 0:
            break
        speed = int(input('Enter the speed: '))
        stop_action = input('Enter the stop action: ')

        spin_right_by_encoders(degrees, speed, stop_action)


def spin_left_seconds(seconds, speed, stop_action):
    """
    Makes the robot spin in place left for the given number of seconds at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the given stop_action.
    """
    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    left_motor.run_forever(speed_sp=speed*8, stop_action=stop_action)
    right_motor.run_forever(speed_sp=-speed*8, stop_action=stop_action)
    time.sleep(seconds)
    left_motor.stop()
    right_motor.stop()


def spin_left_by_time(degrees, speed, stop_action):
    """
    Makes the robot spin in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the algorithm:
      0. Compute the number of seconds to move to achieve the desired distance.
      1. Start moving.
      2. Sleep for the computed number of seconds.
      3. Stop moving.
    """
    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    seconds = degrees * 6.65 / 1.3 / (speed * 8)
    left_motor.run_forever(speed_sp=speed*8, stop_action=stop_action)
    right_motor.run_forever(speed_sp=-speed*8, stop_action=stop_action)
    time.sleep(seconds)
    left_motor.stop()
    right_motor.stop()


def spin_left_by_encoders(degrees, speed, stop_action):
    """
    Makes the robot spin in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the algorithm:
      1. Compute the number of degrees the wheels should spin to achieve the desired distance.
      2. Move until the computed number of degrees is reached.
    """
    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    deg = degrees * 6.65 / 1.3
    left_motor.run_to_rel_pos(position_sp=deg, speed_sp=speed * 8, stop_action=stop_action)
    right_motor.run_to_rel_pos(position_sp=-deg, speed_sp=-speed * 8, stop_action=stop_action)


def spin_right_seconds(seconds, speed, stop_action):
    """ Calls spin_left_seconds with negative speeds to achieve spin_right motion. """
    spin_left_seconds(seconds, -speed, stop_action)


def spin_right_by_time(degrees, speed, stop_action):
    """ Calls spin_left_by_time with negative speeds to achieve spin_right motion. """
    spin_left_by_time(degrees, -speed, stop_action)


def spin_right_by_encoders(degrees, speed, stop_action):
    """ Calls spin_left_by_encoders with negative speeds to achieve spin_right motion. """
    spin_left_by_encoders(degrees, -speed, stop_action)


test_spin_left_spin_right()
