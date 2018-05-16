"""
    This is the final csse120 project file, which is going to be using TKinter GUI driving
    the robot and letting it pick up a red cap on the ground. The robot will use its camera
    looking for a red color and will use its arm picking up a red object, which in this
    case is purposefully set as a red cap. When the robot spots the object and successfully
    picks it up, it will sings a song, and its LED light will become red. After driving it
    to where the user wants the cap to be placed, the robot will put down its arm and says
    "Mission Completed!"

    Arthor: Lilin Chen
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Red Cap Picker")

    main_frame = ttk.Frame(root, padding=50)
    main_frame.grid()
    photo = tkinter.PhotoImage(file='')

    button1 = ttk.Button(main_frame, image=photo)
    # The next line is necessary when your root.mainloop() call is outside the
    # current method. Tkinter has a bug that makes it think the image is ready for
    # garbage collection, which makes the image fully transparent.
    # See: http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
    button1.image = photo
    button1.grid()
    button1['command'] = lambda: print('hello')