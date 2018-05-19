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
        self.color_sensor = ev3.ColorSensor()
        self.running = True
        self.list = []
        self.pixy = ev3.Sensor(driver_name='pixy-lego')
        self.ir_sensor = ev3.InfraredSensor()
        self.running = True

        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor
        assert self.color_sensor
        assert self.pixy
        assert self.ir_sensor


    def forward(self, inches, speed = 100, stop_action = "brake"):
        deg = (inches / (1.3 * 3.14159)) * (2 * 3.14159) * (180 / 3.14159)  # number of revolutions * 2pi rad/rev * 180 deg/pi rad
        self.left_motor.run_to_rel_pos(speed_sp=speed * 8)
        self.right_motor.run_to_rel_pos(speed_sp=speed * 8)
        self.left_motor.run_to_rel_pos(position_sp=deg)
        self.right_motor.run_to_rel_pos(position_sp=deg)

        self.left_motor.wait_while('running')
        self.right_motor.wait_while('running')

    def foreverforward(self, lspeed, rspeed):
        self.left_motor.run_forever(speed_sp=lspeed)
        self.right_motor.run_forever(speed_sp=rspeed)


    def backward(self, inches, speed, stop_action = "brake"):
        if speed < 0:
            self.forward(-inches, speed, stop_action)

    def stop(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def turn_left(self, degrees, speed = 100, stop_action = "brake"):
        distance = (degrees / 360) * 2 * math.pi * 5.75
        wheel_degrees = (distance / (2 * math.pi * 0.75)) * 360
        self.left_motor.run_to_rel_pos(position_sp=wheel_degrees, speed_sp=speed)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.stop_action = stop_action

    def left(self, speed):
        self.right_motor.run_forever(speed_sp=0)
        self.left_motor.run_forever(speed_sp=speed)

    def turn_right(self, degrees, speed, stop_action = "brake"): # speed needs to be negative
        distance = (degrees / 360) * 2 * math.pi * 5.75
        wheel_degrees = (distance / (2 * math.pi * 0.75)) * 360
        self.right_motor.run_to_rel_pos(position_sp=wheel_degrees, speed_sp=-speed)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.stop_action = stop_action


    def right_turn(self, speed):
        self.right_motor.run_forever(speed_sp=speed)
        self.left_motor.run_forever(speed_sp=0)

    def add_to_list(self, direction):
        print('adding')
        self.list.append(direction)

    def printing_list(self):
        print('reached')
        for k in range(len(self.list)):
            print(self.list[k])

    def following(self):
        direction_counter = 0
        # LINE FOLLOWING
        while True:
            self.pixy.mode = 'SIG1'
            print("(X,Y) = ({}, {}) Width = {} Height={}".format(
                self.pixy.value(1), self.pixy.value(2), self.pixy.value(3), self.pixy.value(4)))

            if self.color_sensor.reflected_light_intensity >= 0 and self.color_sensor.reflected_light_intensity < 10:
                lspeed = 600  # This goes straight now, but if you want it to follow a curved path, need to have this step turn it left
                rspeed = 600
                self.foreverforward(lspeed, rspeed)  # Moving forward when intensity in range
                print(self.pixy.value(1))

            elif self.touch_sensor.is_pressed == 1:

                self.left_motor.stop(stop_action="brake")
                self.right_motor.stop(stop_action="brake")
                break

            elif self.pixy.value(1) != 0:  # Robot stops at red
                print('reached1')
                self.left_motor.stop(stop_action="brake")
                self.right_motor.stop(stop_action="brake")

                if direction_counter>len(self.list)-1:
                    print ('Out of directions')

                # CHOOSING WHICH DIRECTION TO GO AT INTERSECTION
                elif self.list[direction_counter] == 'forward':
                    direction_counter =direction_counter + 1
                    pass
                elif self.list[direction_counter] == 'right':
                    direction_counter = direction_counter + 1
                    option = 1
                elif self.list[direction_counter] == 'left':
                    direction_counter = direction_counter + 1
                    option = 2

                self.pixy.mode = 'SIG2'
                var = 1
                while var == 1:

                    if self.pixy.value(1) != 0:
                        print('reached2')
                        if option == 1:
                            self.turn_right(90, 600, "brake")
                        elif option == 2:
                            self.turn_left(90, 600, "brake")
                        break
#
            elif self.color_sensor.reflected_light_intensity > 10:
                print('turning')
                lspeed = 600
                rspeed = 100
                self.foreverforward(lspeed, rspeed)  # Turning right when light intensity out of range
                print(self.pixy.value(1))

    def arm_calibration(self):
#
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

        self.arm_motor.run_forever(speed_sp=800)
        while self.touch_sensor.is_pressed == 0:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()


    def arm_down(self):

        arm_revolutions_for_full_range = 14.2
        deg = 14.2 * 360# Not sure if correct

        self.arm_motor.run_to_rel_pos(speed_sp=800)
        self.arm_motor.run_to_rel_pos(position_sp=-deg)
        ev3.Sound.beep()
        time.sleep(.1)
        self.arm_motor.wait_while(ev3.Motor.STATE_HOLDING)  # Blocks until the motor finishes running

    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def shutdown(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.
        ev3.Sound.speak('Goodbye').wait
        self.running = False

    def sing(self):
        if not self.touch_sensor.is_pressed:
            print("Don't sing")
            ev3.Sound.speak("I will not sing a song until I pick a red cap up").wait()
        if self.touch_sensor.is_pressed:
            print("Sing")
            ev3.Sound.play("/home/robot/csse120/assets/sounds/awesome_pcm.wav").wait()
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)

    def mission_complete(self):
        ev3.Sound.speak("Mission complete")

    def conditions_for_meeting(self):
        self.pixy.mode = "SIG1"
        print("(X, Y) = ({}, {})    Width = {} Height = {}".format(
            self.pixy.value(1), self.pixy.value(2), self.pixy.value(3), self.pixy.value(4)))
        print(self.ir_sensor.proximity)
        time.sleep(0.5)
        while not self.touch_sensor.is_pressed:
            if self.ir_sensor.proximity < 20:
                if self.pixy.value(1) > 188 or self.pixy.value(1) < 199:
                    if self.pixy.value(2) > 70 or self.pixy.value(2) < 130:
                        if self.pixy.value(3) > 4:
                            if self.pixy.value(4) > 1:
                                return True

    def found_it(self):
        print("Picking up!")
        ev3.Sound.play("/home/robot/csse120/assets/sounds/awesome_pcm.wav").wait()
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
