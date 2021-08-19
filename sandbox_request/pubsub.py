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

"""Defines all async pub/sub communication"""

import pika
from ghga_service_chassis_lib.pubsub import AmqpTopic
from .config import get_config


def get_connection_params():
    """Return a configuration object for pika"""
    config = get_config()

    return pika.ConnectionParameters(
        host=config.rabbitmq_host, port=config.rabbitmq_port
    )


def send_message_notification(received_message: dict):
    """Send a message when download request message arrives"""

    config = get_config()

    drs_id = received_message["drs_id"]
    access_id = received_message["access_id"]
    user_id = received_message["user_id"]

    message = {
        "recipient_name": "Recipient",
        "recipient_email": "example@example.com",
        "message": "A new download request ({}) has arrived from user {} with access_id {}".format(
            drs_id, user_id, access_id
        ),
        "subject": "Download request {}".format(drs_id),
    }

    topic = AmqpTopic(
        connection_params=get_connection_params(),
        topic_name=config.sendnotif_topic_name,
        service_name="request",
    )

    topic.publish(message)


def subscribe():
    """Subscribes to the `download_request` topic."""

    config = get_config()

    topic = AmqpTopic(
        connection_params=get_connection_params(),
        topic_name=config.downloadreq_topic_name,
        service_name="request",
    )

    topic.subscribe_for_ever(exec_on_message=send_message_notification)
