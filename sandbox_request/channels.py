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


STORAGE_NOTIFICATION_TOPIC = "storage.notification"


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
