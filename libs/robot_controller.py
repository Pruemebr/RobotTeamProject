"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.running = True

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor
            

    def forward(self, inches, speed, stop_action = "brake"):
        deg = (inches / (1.3 * 3.14159)) * (2 * 3.14159) * (180 / 3.14159)  # number of revolutions * 2pi rad/rev * 180 deg/pi rad
        self.left_motor.run_to_rel_pos(speed_sp=speed * 8)
        self.right_motor.run_to_rel_pos(speed_sp=speed * 8)
        self.left_motor.run_to_rel_pos(position_sp=deg)
        self.right_motor.run_to_rel_pos(position_sp=deg)

        self.left_motor.wait_while('running')
        self.right_motor.wait_while('running')

    def foreverforward(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp = left_motor_speed)
        self.right_motor.run_forever(speed_sp = right_motor_speed)

    def backward(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=-left_motor_speed)
        self.right_motor.run_forever(speed_sp=-right_motor_speed)

    def turn_left(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=-left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)

    def turn_right(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=-right_motor_speed)

    def stop(self):
        self.left_motor.stop_action = "brake"
        self.right_motor.stop_action = "brake"
        self.left_motor.stop()
        self.right_motor.stop()

    def arm_calibration(self):

        self.arm_motor.run_forever(speed_sp=400)
        while self.touch_sensor.is_pressed == 0:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2
        deg = (arm_revolutions_for_full_range / (1.3 * 3.14159)) * (2 * 3.14159) * (180 / 3.14159)
        self.arm_motor.run_to_rel_pos(speed_sp=400)
        self.arm_motor.run_to_rel_pos(position_sp=-deg)

        time.sleep(8)
        ev3.Sound.beep()

        self.arm_motor.wait_while(ev3.Motor.STATE_STALLED)

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):

        arm_revolutions_for_full_range = 14.2
        deg = (arm_revolutions_for_full_range / (1.3 * 3.14159)) * (2 * 3.14159) * (180 / 3.14159)  # Not sure if correct

        self.arm_motor.run_to_rel_pos(speed_sp=800)
        self.arm_motor.run_to_rel_pos(position_sp=-deg)
        ev3.Sound.beep()
        time.sleep(.1)
        self.arm_motor.wait_while(ev3.Motor.STATE_HOLDING)  # Blocks until the motor finishes running

    def arm_down(self):

        arm_revolutions_for_full_range = 14.2
        deg = (arm_revolutions_for_full_range / (1.3 * 3.14159)) * (2 * 3.14159) * (
                    180 / 3.14159)  # Not sure if correct

        self.arm_motor.run_to_rel_pos(speed_sp=800)
        self.arm_motor.run_to_rel_pos(position_sp=-deg)
        ev3.Sound.beep()
        time.sleep(.1)
        self.arm_motor.wait_while(ev3.Motor.STATE_HOLDING)  # Blocks until the motor finishes running

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def shutdown(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.
        self.running = False
        while self.running:
            self.left_motor.stop()
            self.right_motor.stop()