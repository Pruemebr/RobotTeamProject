"""
    This is the final csse120 project file, which is going to be using pc remotely driving
    the robot and letting it pick up a red cap on the ground. The robot will use its camera
    looking for a red color, infrared sensor judging distance between it self and the object,
    and will use its arm picking up a red object, which in this case is purposefully set as
    a red cap. When the robot detects the object and successfully picks it up, it will sing
    a song, and its LED light will become red. After driving it to where the user wants the
    cap to be placed, the robot will put down its arm and says "Mission Completed!"

    Arthor: Lilin Chen
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Red Cap Grabber")

    main_frame = ttk.Frame(root, padding=90)
    main_frame.grid()

    photo = tkinter.PhotoImage(file='redcap.gif')

    button1 = ttk.Button(main_frame, image=photo, padding=100)
    button1.image = photo
    button1.grid(row=0)
    button1['command'] = lambda: print('I am a cap')

    start_button = ttk.Button(main_frame, text='Start the Program')
    start_button.grid(row=1)
    start_button['command'] = lambda: pop_up_control_board()

    root.mainloop()


def pop_up_control_board():
    control_board = tkinter.Toplevel()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    control_board.title("Red Cap Grabber Control Board")
    main_frame = ttk.Frame(control_board, padding=50)
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "900")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "900")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: forward(mqtt_client, left_speed_entry, right_speed_entry)

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: turn_left(mqtt_client, left_speed_entry, right_speed_entry)

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: stop(mqtt_client)

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: turn_right(mqtt_client, left_speed_entry, right_speed_entry)

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: backward(mqtt_client, left_speed_entry, right_speed_entry)

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    s_button = ttk.Button(main_frame, text="Sing")
    s_button.grid(row=5, column=0)
    s_button['command'] = (lambda: sing(mqtt_client))

    control_board.mainloop()


def forward(mqtt_client, left_speed_entry, right_speed_entry):
    l_speed = int(left_speed_entry.get())
    r_speed = int(right_speed_entry.get())
    print("Forward!")
    mqtt_client.send_message("foreverforward", [l_speed, r_speed])


def turn_left(mqtt_client, left_speed_entry, right_speed_entry):
    l_speed = int(left_speed_entry.get())
    r_speed = int(right_speed_entry.get())
    print("Turning Left!")
    mqtt_client.send_message("right_turn", [r_speed])


def stop(mqtt_client):
    print("Stop!")
    mqtt_client.send_message("stop")


def turn_right(mqtt_client, left_speed_entry, right_speed_entry):
    l_speed = int(left_speed_entry.get())
    r_speed = int(right_speed_entry.get())
    print("Turning Right!")
    mqtt_client.send_message("left", [l_speed])


def backward(mqtt_client, left_speed_entry, right_speed_entry):
    l_speed = -int(left_speed_entry.get())
    r_speed = -int(right_speed_entry.get())
    print("Backward!")
    mqtt_client.send_message("foreverforward", [l_speed, r_speed])


def quit_program(mqtt_client, shutdown_ev3):
    print("mission complete")
    mqtt_client.send_message("arm_down")
    mqtt_client.send_message("mission_complete")
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def sing(mqtt_client):
    mqtt_client.send_message("sing")


main()