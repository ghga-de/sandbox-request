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

from typing import List, Dict
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from sandbox_request.dao.request import (
    get_all_requests,
    get_request,
    add_request,
    update_request,
    delete_request,
)
from sandbox_request.models import Request
from sandbox_request.core.process_requests import approve_request, reject_request


request_router = APIRouter()


@request_router.get("/requests", response_model=List[Request])
async def get_requests():
    """get requests

    Returns: requests
    """
    requests = await get_all_requests()
    return requests


@request_router.get("/requests/{request_id}", response_model=Request)
async def get_one_request(request_id):
    """get one request

    Args:
        request_id ([type]): [description]

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    request = await get_request(request_id)
    if not request:
        raise HTTPException(
            status_code=404, detail=f"Request with id '{request_id}' not found"
        )
    return request


@request_router.post("/requests", response_model=Request)
async def add_requests(data: Dict):
    """add request

    Args:
        data (Dict): [description]

    Returns:
        [type]: [description]
    """
    request = await add_request(data)
    return request


@request_router.put("/requests/{request_id}", response_model=Request)
async def update_requests(request_id, data: Dict):
    """update request

    Args:
        request_id ([type]): [description]
        data (Dict): [description]

    Returns:
        [type]: [description]
    """
    request = await update_request(request_id, data)
    return request


@request_router.delete("/requests/{request_id}", response_model=Request)
async def delete_requests(request_id):
    """delete request

    Args:
        request_id ([type]): [description]
    """
    await delete_request(request_id=request_id)


@request_router.post("/approveRequests/{request_id}", response_model=Request)
async def approve_requests(request_id: str):
    """calls approve_request from process_requests

    Args:
        request_id (str): request_id
    """
    await approve_request(request_id)


@request_router.post("/rejectRequests/{request_id}", response_model=Request)
async def reject_requests(request_id: str):
    """calls reject_request from process_requests

    Args:
        request_id (str): [description]
    """
    await reject_request(request_id)
