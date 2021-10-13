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

"""
All routes for interacting with Data Requests.
"""

from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.params import Depends

from sandbox_request.dao.request import (
    add_request,
    delete_request,
    get_all_requests,
    get_request,
    update_request,
)
from sandbox_request.core.utils import check_dataset
from sandbox_request.models import RequestInit, Request, RequestPartial
from sandbox_request.pubsub import send_notification
from sandbox_request.config import get_config


request_router = APIRouter()


@request_router.get("/requests", response_model=List[Request])
async def get_requests():
    """
    Retrieve a list of Request objects from the metadata store.
    """
    requests = await get_all_requests()
    return requests


@request_router.get("/requests/{request_id}", response_model=Request)
async def get_one_request(request_id):
    """
    Given a Request ID, get the Request object.
    """
    request = await get_request(request_id)
    if not request:
        raise HTTPException(
            status_code=404, detail=f"Request with id '{request_id}' not found"
        )
    return request


@request_router.post("/requests", response_model=Request)
async def add_requests(data: RequestInit, config=Depends(get_config)):
    """
    Add a new Request.
    """
    dataset_id = data.dataset_id
    await check_dataset(dataset_id)
    request = await add_request(data)
    send_notification(
        recipient_name=config.data_steward_name,
        recipient_email=config.data_steward_email,
        subject=f"New Request Created: {request.id}",
        message_text=(
            f"User {request.user_id} created a new request {request.id} "
            f"to access dataset {request.dataset_id}."
        ),
    )
    return request


@request_router.patch("/requests/{request_id}", response_model=Request)
async def update_requests(request_id, data: RequestPartial, config=Depends(get_config)):
    """
    Given a Request ID and data, update the Request object.
    """
    request = await update_request(request_id, data)
    send_notification(
        recipient_name=config.data_requester_name,
        recipient_email=config.data_requester_email,
        subject=f"Request Updated: {request.id}",
        message_text=(
            f"The request {request.id} has been updated to:\n\n"
            f"Purpose: {request.purpose}\n\n"
            f"Status: {request.status}"
        ),
    )
    return request


@request_router.delete("/requests/{request_id}", response_model=Request)
async def delete_requests(request_id, config=Depends(get_config)):
    """
    Delete a Request object based on Request ID.
    """
    await delete_request(request_id)
    send_notification(
        recipient_name=config.data_steward_name,
        recipient_email=config.data_steward_email,
        subject=f"Request Updated: {request_id}",
        message_text=f"The request {request_id} has been deleted.",
    )
