"""
    Module channels.py
"""
# Copyright 2021 Universität Tübingen, DKFZ and EMBL
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import pika

REQUEST_NOTIFICATION_TOPIC = "request-notification"
STORAGE_REQUEST_TOPIC = "request-notification"
STORAGE_REQUEST_QUEUE = "storage-request"
EXCHANGE_STORAGE = "storage"
EXCHANGE_REQUEST = "request"
TOPIC = "topic"


def send_mail(user_id: str, message: str):
    """Call the notification service to send mail to the user

    Args:
        user_id (str): recipient mail id
        message (str): message to be sent
    """
    print(user_id, message)
    # sandbox_notification.core.send_mail(user_id, message)


def subscribe_to_storage():
    """
    call the sandbox_notification.topics.subscribe()
    """
    # sandbox_notification.topics.subscribe(STORAGE_NOTIFICATION_TOPIC)
    subscribe(EXCHANGE_STORAGE, STORAGE_REQUEST_TOPIC, STORAGE_REQUEST_QUEUE)


def publish_topic(message):
    """
    Run a test for publishing a notification.
    """
    message_obj = {"msg": message}

    msg_json = json.dumps(message_obj)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.exchange_declare(exchange="request", exchange_type=TOPIC)
    channel.basic_publish(
        exchange="request",
        routing_key=REQUEST_NOTIFICATION_TOPIC,
        body=msg_json,
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()


def callback(
    channel: pika.channel.Channel,
    method: pika.spec.Basic.Deliver,
    _: pika.spec.BasicProperties,
    body: str,
):
    """
    Executed once a message is received
    """

    message_obj = json.loads(body)
    user_id = "user"
    try:
        # write to db
        send_mail(user_id, message_obj)
    except ValueError:
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    else:
        channel.basic_ack(delivery_tag=method.delivery_tag)


def subscribe(exchange, topic_str, queue):
    """
    Subscribe this consumer to a topic or set of topics based on a
    topic string as defined in the AMQP 0.9.1 specification.
    """

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type=TOPIC)

    result = channel.queue_declare(queue=queue, durable=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=exchange, queue=queue, routing_key=topic_str)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()
