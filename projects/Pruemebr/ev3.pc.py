#import tkinter
#from tkinter import ttk

import mqtt_remote_method_calls as com
import robot_controller as robo

def main():
    bot = robo.Snatch3r()
    mqtt_client = com.MqttClient(bot)
    mqtt_client.connect_to_pc()
    #mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    bot.loop_forever()
main()
# direction_counter = 0
# #LINE FOLLOWING
# while True:
#     pixy.mode = 'SIG1'
#     print("(X,Y) = ({}, {}) Width = {} Height={}".format(
#         pixy.value(1), pixy.value(2), pixy.value(3), pixy.value(4)))
#
#
#     if color_sensor.reflected_light_intensity >=0 and color_sensor.reflected_light_intensity < 10:
#         lspeed = 600 #This goes straight now, but if you want it to follow a curved path, need to have this step turn it left
#         rspeed = 600
#         bot.foreverforward(lspeed, rspeed) #Moving forward when intensity in range
#         print(pixy.value(1))
#
#     elif touch_sensor.is_pressed == 1:
#
#         bot.left_motor.stop(stop_action = "brake")
#         bot.right_motor.stop(stop_action = "brake")
#         break
#
#     elif pixy.value(1) != 0: #Robot stops at red
#         print('reached1')
#         bot.left_motor.stop(stop_action="brake")
#         bot.right_motor.stop(stop_action="brake")
#
#         #CHOOSING WHICH DIRECTION TO GO AT INTERSECTION
#         if bot.list[direction_counter] == 'forward':
#             pass
#         elif bot.list[direction_counter] == 'right':
#             option = 1
#         elif bot.list[direction_counter] == 'left':
#             option = 2
#
#         pixy.mode = 'SIG2'
#         var = 1
#         while var==1:
#
#             if pixy.value(1) != 0:
#                 print('reached2')
#                 if option == 1:
#                     bot.turn_right(90, -600, "brake")
#                 elif option == 2:
#                     bot.turn_left(90, -600, "brake")
#                 break
#
#     elif color_sensor.reflected_light_intensity >10:
#         print('turning')
#         lspeed = 600
#         rspeed = 100
#         bot.foreverforward(lspeed, rspeed) #Turning right when light intensity out of range
#         print(pixy.value(1))
#
#
#
#
# #LINE FOLLOWING
#



