# This project is meant to prevent the robot from knocking into obstacles in the front. When the distance from the robot
# to the obstacle is less than 50 cm, the LEDs will be yellow. When the distance is less than 30 cm, the LEDs will be
# red and the robot cannot move forward. The user can get the distance by clicking a button on the Tkinter GUI.

# Author: Zikang Zhang

# Since the class in robot_controller.py is messy, I made another class in this file for my own use.

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time


class Snatch3r(object):

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.Leds = ev3.Leds
        self.infrared_sensor = ev3.InfraredSensor()
        self.mqtt_client = None
        self.running = True

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.infrared_sensor

    def forward(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)
        while True:
            proximity = self.infrared_sensor.proximity
            if proximity < 70 and proximity >= 42:
                self.Leds.set_color(self.Leds.LEFT, self.Leds.YELLOW)
                self.Leds.set_color(self.Leds.RIGHT, self.Leds.YELLOW)
            elif proximity < 42:
                self.left_motor.stop()
                self.right_motor.stop()
                self.Leds.set_color(self.Leds.LEFT, self.Leds.RED)
                self.Leds.set_color(self.Leds.RIGHT, self.Leds.RED)
                break

    def backward(self, left_motor_speed, right_motor_speed):
        self.Leds.set_color(self.Leds.LEFT, self.Leds.BLACK)
        self.Leds.set_color(self.Leds.RIGHT, self.Leds.BLACK)
        self.left_motor.run_forever(speed_sp=-left_motor_speed)
        self.right_motor.run_forever(speed_sp=-right_motor_speed)

    def turn_left(self, left_motor_speed, right_motor_speed):
        self.Leds.set_color(self.Leds.LEFT, self.Leds.BLACK)
        self.Leds.set_color(self.Leds.RIGHT, self.Leds.BLACK)
        self.left_motor.run_forever(speed_sp=-left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)

    def turn_right(self, left_motor_speed, right_motor_speed):
        self.Leds.set_color(self.Leds.LEFT, self.Leds.BLACK)
        self.Leds.set_color(self.Leds.RIGHT, self.Leds.BLACK)
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=-right_motor_speed)

    def stop(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        self.Leds.set_color(self.Leds.LEFT, self.Leds.BLACK)
        self.Leds.set_color(self.Leds.RIGHT, self.Leds.BLACK)

    def shutdown(self):
        self.running = False
        self.Leds.set_color(self.Leds.LEFT, self.Leds.BLACK)
        self.Leds.set_color(self.Leds.RIGHT, self.Leds.BLACK)
        self.right_motor.stop()
        self.left_motor.stop()

    def distance(self):
        distance = self.infrared_sensor.proximity / 100 * 70
        self.mqtt_client.send_message('print_distance', [distance])

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)


def main():
    robot = Snatch3r()
    mqtt_client = com.MqttClient(robot)
    robot.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    robot.loop_forever()


main()
