# Run from project root:
# python mqtt_services/mqtt_ai_service.py


import os
import threading

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from ai_tools.ai_client import ask_ai
from ai_tools.status_tool import get_latest_status
from ai_tools.heatpump_mapping import get_heatpump_id

load_dotenv("/home/sct/smartgate/config.env")

MQTT_HOST = os.getenv("MQTT_HOST", "server")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1888))

QUESTION_TOPIC = "sct/heatpump/+/ai/question"


def get_full_number_from_topic(topic):
    return topic.split("/")[2]


def handle_message(client, topic, question):
    full_number = get_full_number_from_topic(topic)
    answer_topic = f"sct/heatpump/{full_number}/ai/answer"

    heatpump_id = get_heatpump_id(full_number)
    if heatpump_id is None:
        msg = f"Unknown SmartGate full number: {full_number}"
        client.publish(answer_topic, msg)
        print(msg)
        return

    print(f"Question [{full_number}]: {question}")

    status = get_latest_status(heatpump_id)
    answer = ask_ai(f"User question:\n{question}\n\nLatest heat pump status:\n{status}")

    client.publish(answer_topic, answer)
    print(f"Answer published to: {answer_topic}\n{answer}")


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT:", rc)
    client.subscribe(QUESTION_TOPIC)
    print("Subscribed to:", QUESTION_TOPIC)


def on_message(client, userdata, msg):
    topic = msg.topic
    question = msg.payload.decode("utf-8")
    threading.Thread(
        target=handle_message, args=(client, topic, question), daemon=True
    ).start()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)

print("SmartGate AI MQTT service started")
client.loop_forever()
