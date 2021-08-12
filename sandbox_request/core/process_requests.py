"""
    Module requests.py
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

from sandbox_request.dao.request import get_request, update_request
from sandbox_request.channels import send_mail


async def approve_request(request_id: str):
    """
    approves a request.

    Args:
        request_id (str): id of the request.
    """
    request = await get_request(request_id)
    user_id = request["user_id"]
    dataset_id = request["dataset_id"]
    if request["status"] in ["requested", "rejected"]:
        await update_request(request_id, {"status": "approved"})
    send_mail(user_id, "request approved for dataset " + dataset_id)


async def reject_request(request_id: str):
    """
    rejects a request.

    Args:
        request_id (str): id of the request.
    """
    request = await get_request(request_id)
    user_id = request["user_id"]
    dataset_id = request["dataset_id"]
    if request["status"] == "requested":
        await update_request(request_id, {"status": "rejected"})
    send_mail(user_id, "request rejected for dataset " + dataset_id)


async def get_all_datasets():
    """
    get all datasets from metadata service
    """
    # sandbox_metadata.metadata_service.routes.get_all_datasets()
