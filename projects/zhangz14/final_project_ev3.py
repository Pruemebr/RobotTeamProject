import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time


class Snatch3r(object):

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor
        self.Leds = ev3.Leds
        self.infrared_sensor = ev3.InfraredSensor()
        self.running = True

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.infrared_sensor
        assert self.touch_sensor

    def forward(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)
        proximity = self.infrared_sensor.proximity
        if proximity < 70:
            self.Leds.set_color(self.Leds.LEFT, self.Leds.YELLOW)
            self.Leds.set_color(self.Leds.RIGHT, self.Leds.YELLOW)
        if proximity < 40:
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
        self.right_motor.stop()
        self.left_motor.stop()

    def arm_up(self):
        deg = 10 * 360
        self.arm_motor.run_to_rel_pos(speed_sp=800)
        self.arm_motor.run_to_rel_pos(position_sp=deg)
        self.arm_motor.wait_while(self.arm_motor.STATE_RUNNING)
        self.arm_motor.stop()

    def arm_down(self):

        deg = 10 * 360

        self.arm_motor.run_to_rel_pos(speed_sp=800)
        self.arm_motor.run_to_rel_pos(position_sp=-deg)
        self.arm_motor.wait_while(self.arm_motor.STATE_RUNNING)
        self.arm_motor.stop()


def main():
    robot = Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    time.sleep(0.1)


main()
