
#Robotics Midterm Robot allow for user control until object is detected within certain range then diverts course unitl path is clear then allows for user control once more

import threading
import signal
import queue
import gopigo3
from curtsies import Input
from time import sleep
from easygopigo3 import *
import picamera 
robot = EasyGoPiGo3()
robot.reset_encoders()
MINIMUM_VOLTAGE = 7.0
MOTORS_SPEED = 99999

# Keyboard controls
def robotControl(trigger, simultaneous_launcher, motor_command_queue, sensor_queue):
    time_to_wait_in_queue = 0.1 
    try:
        robot = EasyGoPiGo3()
        i = 0
        my_distance_sensor = robot.init_distance_sensor()
    except IOError:
        print("GoPiGo3 robot not detected")
        simultaneous_launcher.abort()
    except gopigo3.FirmwareVersionError:
        print("GoPiGo3 board needs to be updated")
        simultaneous_launcher.abort()
    except Exception:
        print("Unknown error occurred while instantiating GoPiGo3")
        simultaneous_launcher.abort()
    try:
        simultaneous_launcher.wait()
    except threading.BrokenBarrierError as msg:
        print("[robotControl] thread couldn't be launched")
    if not simultaneous_launcher.broken:
        robot.stop()
        robot.set_speed(MOTORS_SPEED)
    direction_degrees = 0
    move = 0
    command = "stop"
    record = False
    while not (trigger.is_set() or simultaneous_launcher.broken or robot.volt() <= MINIMUM_VOLTAGE):
        try:
            command = motor_command_queue.get(timeout = time_to_wait_in_queue)
        except queue.Empty:
            pass
            move = False
        print("Total Distance:" +str(robot.read_encoders_average()) +"mm")
        dist_value = my_distance_sensor.read_mm()
        print("Obstacle Distance: {} mm ".format(my_distance_sensor.read_mm()))  
        if(dist_value>=200):
            if command == "STOP":
                move = 0    
            if command == "LEFT":
                robot.turn_degrees(-15)
            elif command == "RIGHT":
                robot.turn_degrees(15)
            elif command == "FORWARD":
                move = 1;
            elif command == "BACKWARDS":
                robot.turn_degrees(180) 
            command = "STOP"
        else:
            move = -1;
        if move == 0:
            robot.stop()
        elif move == -1:
            print("Obstacle detected. Diverting course.")
            robot.drive_cm(-20)
            robot.turn_degrees(45)
        else:
            robot.forward() 
        sleep(0.001)
    if not simultaneous_launcher.broken:
        robot.stop()

def record():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_recording('session.h264')
        camera.wait_recording(120)
        camera.stop_recording()

def Main(trigger):
    simultaneous_launcher = threading.Barrier(2) 
    motor_command_queue = queue.Queue(maxsize = 1) 
    sensor_queue = queue.Queue(maxsize = 1) 
    keyboard_refresh_rate = 20.0 
    available_commands = {"<LEFT>": "LEFT",
                          "<RIGHT>": "RIGHT",
                          "<UP>": "FORWARD",
                          "<DOWN>": "BACKWARDS",
                          "<SPACE>": "STOP"}
    menu_order = ["<LEFT>", "<RIGHT>", "<UP>", "<DOWN>", "<SPACE>"] 
    print("   _____       _____ _  _____         ____  ")
    print("  / ____|     |  __ (_)/ ____|       |___ \ ")
    print(" | |  __  ___ | |__) || |  __  ___     __) |")
    print(" | | |_ |/ _ \|  ___/ | | |_ |/ _ \   |__ < ")
    print(" | |__| | (_) | |   | | |__| | (_) |  ___) |")
    print("  \_____|\___/|_|   |_|\_____|\___/  |____/ ")
    print("                                            ")
    robotcontrol_thread = threading.Thread(target = robotControl, args = (trigger, simultaneous_launcher, motor_command_queue, sensor_queue))
    record_thread = threading.Thread(target = record)
    robotcontrol_thread.start()
    record_thread.start()
    try:
        simultaneous_launcher.wait()
        print("Ready to go.")
        for menu_command in menu_order:
            print("{:8} - {}".format(menu_command, available_commands[menu_command]))
    except threading.BrokenBarrierError:
        pass
    with Input(keynames = "curtsies") as input_generator:
        while not (trigger.is_set() or simultaneous_launcher.broken):
            period = 1 / keyboard_refresh_rate
            key = input_generator.send(period)
            if key in available_commands:
                try:
                    motor_command_queue.put_nowait(available_commands[key])
                except queue.Full:
                    pass
    if simultaneous_launcher.broken:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    trigger = threading.Event() # event used when CTRL-C is pressed
    signal.signal(signal.SIGINT, lambda signum, frame : trigger.set()) # SIGINT (CTRL-C) signal handler
    Main(trigger)
