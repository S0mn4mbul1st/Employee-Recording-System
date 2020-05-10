import paho.mqtt.client as mqtt

client = mqtt.Client()
while True:

    client.publish("work/records")
    client.publish("task/records")

