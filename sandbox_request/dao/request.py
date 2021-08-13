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
    Wrappers around DB queries related to requests
"""

from typing import Union, List
from sandbox_request.dao.db_connect import Database
from sandbox_request.channels import send_mail
from sandbox_request.models import Request, RequestPartial

COLLECTION_NAME = "requests"


async def get_all_requests() -> List[Request]:
    """
    get list of all requests

    Returns:
        object:
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    request_dicts = await collection.find().to_list(None)  # type: ignore
    requests = [Request(**request_dict) for request_dict in request_dicts]
    return requests


async def get_request(request_id: str) -> Request:
    """
    get request
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    request_dict = await collection.find_one({"id": request_id})  # type: ignore
    request = Request(**request_dict)
    return request


async def add_request(data: Request) -> Request:
    """
    add new request
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    request_id = data.id
    await collection.insert_one(data.dict())  # type: ignore
    request = await get_request(request_id)
    send_mail("data_steward", "request_made")
    return request


async def update_request(
    request_id: str, data: Union[Request, RequestPartial]
) -> Request:
    """
    update a request
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    collection.update_one(  # type: ignore
        {"id": request_id}, {"$set": data.dict(exclude_unset=True)}
    )
    request_dict = await collection.find_one({"id": request_id})  # type: ignore
    request = Request(**request_dict)
    return request


async def delete_request(request_id: str):
    """
    delete a request
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    collection.delete_one({"id": request_id})  # type: ignore
