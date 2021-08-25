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


def send_notification(
    recipient_name: str, recipient_email: str, subject: str, message_text: str
):
    """Send an email by publishing to the corresponding topic."""

    config = get_config()

    message_text_wrapped = f"""
        Dear {recipient_name},

        {message_text}

        Best wishes,
        The GHGA System
        """

    message = {
        "recipient_name": recipient_name,
        "recipient_email": recipient_email,
        "subject": subject,
        "message": message_text_wrapped,
    }

    topic = AmqpTopic(
        connection_params=get_connection_params(),
        topic_name=config.topic_name_send_notification,
        service_name="request",
    )

    topic.publish(message)


def send_notification_on_download_request(received_message: dict):
    """Send an email upon receiving a message describing a download request event."""

    config = get_config()

    send_notification(
        recipient_name=config.data_steward_name,
        recipient_email=config.data_steward_email,
        subject=f"Download requested: {received_message['drs_id']}",
        message_text=(
            f"User {received_message['user_id']} requested "
            f"the DRS object {received_message['drs_id']} for download "
            f"using the access method {received_message['access_id']}."
        ),
    )


def subscribe():
    """Subscribes to the `download_request` topic."""

    config = get_config()

    topic = AmqpTopic(
        connection_params=get_connection_params(),
        topic_name=config.topic_name_download_requested,
        service_name="request",
    )

    topic.subscribe_for_ever(exec_on_message=send_notification_on_download_request)
