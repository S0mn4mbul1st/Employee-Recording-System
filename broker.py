import paho.mqtt.publish as publish

while True:
    message = input("Please enter your message: ")
    publish.single("work/records", message, hostname="test.mosquitto.org")
    print("Command sent!")

    #comment