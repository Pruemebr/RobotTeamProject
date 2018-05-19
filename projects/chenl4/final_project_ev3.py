"""
    This is the ev3 file for the final project "Red Cap Picker". Run it on a SSH session, and
    run the pc file on your computer.

    Arthor: Lilin Chen
"""

import mqtt_remote_method_calls as com
import robot_controller as robo

def main():
    robot = robo.Snatch3r()

    while robot.running:
        if robot.conditions_for_meeting() == True:
            robot.arm_up()
            robot.found_it()
            break

    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    robot.loop_forever()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()