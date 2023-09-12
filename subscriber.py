# python 3.11

import random
import os
from paho.mqtt import client as mqtt_client
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()

broker = os.getenv("BROKER")
port = int(os.getenv("PORT"))
topic = os.getenv("TOPIC")
if os.getenv("USER_NAME") is None or os.getenv("USER_NAME") == "":
    user_name = None
    pass_word = None
else:
    user_name = os.getenv("USER_NAME")
    pass_word = os.getenv("PASSWORD")

# Generate a Client ID with the publish prefix.
client_id = f"publish-{random.randint(0, 1000)}"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(user_name, pass_word)
    client.on_connect = on_connect
    client.connect(broker, port)
    # client.connect_async(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        try:
            print(
                Fore.WHITE
                + "TOPIC: "
                + Fore.LIGHTYELLOW_EX
                + msg.topic
                + Fore.WHITE
                + "\tDATA: "
                + Fore.GREEN
                + msg.payload.decode("utf-8", "ignore")
            )

        except Exception as e:
            print("there was a problme processing this message", exc_info=e)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    try:
        client.loop_forever()
    except:
        print("application has shutdown")


if __name__ == "__main__":
    run()
