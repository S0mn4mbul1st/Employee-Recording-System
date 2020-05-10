import sys
import re
from activity_service import Service
import paho.mqtt.client as mqtt

service = Service("activities.db")


def start(args):
    return service.start(*args)

def stop(args):
    return service.stop()

def listactivities(args):
    return service.activities(*args)

def upd(args):
    return service.editID(*args)

def askstopifneeds():
    if service.current_activity:
        # ask to stop the current activity
        while (True):
            print('Q: do you want to stop the current activity named "' + service.current_activity + '"? [Y/N]')
            # read command
            command_line = sys.stdin.readline()

            if (command_line == "y\n" or command_line == "Y\n" or command_line == "y" or command_line == "Y"):
                print(service.stop())
                break
            elif (command_line == "n\n" or command_line == "N\n" or command_line == "n" or command_line == "N"):
                break

def exit(args):
    askstopifneeds()
    service.dispose()
    sys.exit()


def exit_immediately(args):
    service.dispose()
    sys.exit()


actions = {
    "start": start,
    "stop"	:	stop,
    "list"	:	listactivities,
    "exit"	:	exit,
}

def getCommands():
 client = mqtt.Client()
 def on_connect(client, userData, flags, rc):
     client.tls_set("ca.crt")
     client.username_pw_set(username="admin", password="admin")
     client.on_message = on_message
     client.on_connect = on_connect
     client.connect("DESKTOP-DTK1T07", 8883, 60)
     print("Connection is successful: " + str(rc))
     client.subscribe("work/records")

 def on_message(client, userData, msg):
    print(msg.topic + ": " + str(msg.payload.decode('utf-8')))
    command_line = str(msg.payload.decode('utf-8'))
    print("Message from the Server", command_line)
    command = re.split("[ ]+", command_line)
    chosenCommand = actions.get(command[0])
    if chosenCommand:
        print(chosenCommand(command[1:]))
    else:
        print("ERROR: unknown command")


 while True:
        message = input("Please enter your message: ")
        client.publish("employee/records", message)
        command_line = message
        command = re.split("[ ]+", command_line)
        chosenCommand = actions.get(command[0])
        if chosenCommand:
            print(chosenCommand(command[1:]))
        else:
            print("ERROR!")

 client.loop_forever()

getCommands()