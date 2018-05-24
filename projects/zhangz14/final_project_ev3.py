# This project is meant to prevent the robot from knocking into obstacles in the front. When the distance from the robot
# to the obstacle is less than 50 cm, the LEDs will be yellow. When the distance is less than 20 cm, the LEDs will be
# red and the robot cannot move forward. The user can get the distance by clicking a button on the Tkinter GUI.

# Author: Zikang Zhang

# Since the class in robot_controller.py is messy, I made another class in this file for my own use.

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time


class Snatch3r(object):

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.Leds = ev3.Leds
        self.infrared_sensor = ev3.InfraredSensor()

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.infrared_sensor

    def forward(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)
        proximity = self.infrared_sensor.proximity
        if proximity < 70:
            self.Leds.set_color(self.Leds.LEFT, self.Leds.YELLOW)
            self.Leds.set_color(self.Leds.RIGHT, self.Leds.YELLOW)
        if proximity < 28:
            self.stop()
            self.Leds.set_color(self.Leds.LEFT, self.Leds.RED)
            self.Leds.set_color(self.Leds.RIGHT, self.Leds.RED)

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
        self.left_motor.stop()
        self.right_motor.stop()
        self.Leds.set_color(self.Leds.LEFT, self.Leds.BLACK)
        self.Leds.set_color(self.Leds.RIGHT, self.Leds.BLACK)

    def shutdown(self):
        self.right_motor.stop()
        self.left_motor.stop()

    def distance(self):
        distance = self.infrared_sensor.proximity / 100 * 70
        return distance


def main():
    robot = Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    time.sleep(0.1)


main()
