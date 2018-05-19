import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com



#Defining functions used by buttons
def start(mqtt_client):
    mqtt_client.send_message('following', [])

def add_forward(mqtt_client):
    print('reached')
    mqtt_client.send_message('add_to_list',['forward'])

def add_left(mqtt_client):
    mqtt_client.send_message('add_to_list', ['left'])


def add_right(mqtt_client):
    mqtt_client.send_message('add_to_list', ['right'])

def print_list(mqtt_client):
    mqtt_client.send_message('printing_list', [])

def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()

def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    #Directions
    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: add_forward(mqtt_client)
    root.bind('<Up>', lambda event: add_forward(mqtt_client))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: add_left(mqtt_client)
    root.bind('<Left>', lambda event: add_left(mqtt_client))
    # left_button and '<Left>' key

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: add_right(mqtt_client)
    root.bind('<Right>', lambda event: add_right(mqtt_client))
    # right_button and '<Right>' key

    print_button = ttk.Button(main_frame, text="Print List")
    print_button.grid(row=4, column=1)
    print_button['command'] = lambda: print_list(mqtt_client)
    root.bind('<p>', lambda event: print_list(mqtt_client))

    start_button = ttk.Button(main_frame, text="Start")
    start_button.grid(row=3, column=1)
    start_button['command'] = lambda: start(mqtt_client)
    root.bind('<space>', lambda event: start(mqtt_client))


    #QUIT AND EXIT
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=6, column=0)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


main()