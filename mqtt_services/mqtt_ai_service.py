# Run from project root:
# python mqtt_services/mqtt_ai_service.py

import logging
import os
import threading
from datetime import date

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from ai_tools.ai_client import ask_ai
from ai_tools.heatpump_mapping import get_heatpump_id

load_dotenv("/home/sct/smartgate/config.env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

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
        log.warning(msg)
        return

    log.info("Question [%s]: %s", full_number, question)

    try:
        today = date.today()
        answer = ask_ai(
            f"heatpump_id: {heatpump_id}\n"
            f"Today's date: {today}\n\n"
            f"User question: {question}"
        )

        client.publish(answer_topic, answer)
        log.info("Answer published to %s", answer_topic)
    except Exception:
        log.exception("Failed to handle message for %s", full_number)


def on_connect(client, userdata, flags, rc):
    log.info("Connected to MQTT broker (rc=%s)", rc)
    client.subscribe(QUESTION_TOPIC)
    log.info("Subscribed to %s", QUESTION_TOPIC)


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

log.info("SmartGate AI MQTT service started")
client.loop_forever()
