#!/usr/bin/env python3
"""
For the full problem statement and details see the corresponding m5_pc_remote_drive.py comments.

There are many solutions to this problem.  The easiest solution on the EV3 side is to NOT bother makes a wrapper
class for the robot object.  Since the challenge presented is very direct it's easiest to just use the Snatch3r class
directly as the delegate to the MQTT client.

The code below is all correct.  The loop_forever line will cause a crash right now.  You need to implement that function
in the Snatch3r class in the library (remember the advice from the lecture).  Pick one team member to implement it then
have everyone else Git update.  Here is some advice for the Snatch3r method loop_forever and it's partner, shutdown.

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

Additionally you will discover a need to create methods in your Snatch3r class to support drive, shutdown, stop, and
more. Once the EV3 code is ready, run it on the EV3 you can work on the PC side code for the MQTT Remote Control.

Author: David Fisher.
"""
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
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

    def forward(self, inches, speed, stop_action="brake"):
        deg = (inches / (1.3 * 3.14159)) * (2 * 3.14159) * (
                    180 / 3.14159)  # number of revolutions * 2pi rad/rev * 180 deg/pi rad
        self.left_motor.run_to_rel_pos(speed_sp=speed * 8)
        self.right_motor.run_to_rel_pos(speed_sp=speed * 8)
        self.left_motor.run_to_rel_pos(position_sp=deg)
        self.right_motor.run_to_rel_pos(position_sp=deg)

        self.left_motor.wait_while('running')
        self.right_motor.wait_while('running')

    def foreverforward(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)

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
        deg = (arm_revolutions_for_full_range / (1.3 * 3.14159)) * (2 * 3.14159) * (
                    180 / 3.14159)  # Not sure if correct

        self.arm_motor.run_to_rel_pos(speed_sp=800)
        self.arm_motor.run_to_rel_pos(position_sp=-deg)
        ev3.Sound.beep()
        time.sleep(.1)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running

    def arm_down(self):

        arm_revolutions_for_full_range = 14.2
        deg = (arm_revolutions_for_full_range / (1.3 * 3.14159)) * (2 * 3.14159) * (
                180 / 3.14159)  # Not sure if correct

        self.arm_motor.run_to_rel_pos(speed_sp=800)
        self.arm_motor.run_to_rel_pos(position_sp=-deg)
        ev3.Sound.beep()
        time.sleep(.1)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running

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

def main():
    robot = Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker

    robot.loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
