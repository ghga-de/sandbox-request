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
from sandbox_request.dao.db_connect import DBConnect
from sandbox_request.models import Request, RequestPartial, StatusEnum

COLLECTION_NAME = "requests"
COUNTER = "counter"


async def get_all_requests() -> List[Request]:
    """
    get list of all requests

    Returns:
        List of Requests
    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(name=COLLECTION_NAME)
    request_dicts = await collection.find().to_list(None)  # type: ignore
    requests = [Request(**request_dict) for request_dict in request_dicts]
    await db_connect.close_db()
    return requests


async def get_request(request_id: str) -> Request:
    """
    get request
    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(name=COLLECTION_NAME)
    request_dict = await collection.find_one({"id": request_id})  # type: ignore
    request = Request(**request_dict)
    await db_connect.close_db()
    return request


async def add_request(data: Request) -> Request:
    """
    add new request
    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(name=COLLECTION_NAME)
    request_id = await get_next_request_id(COUNTER, COLLECTION_NAME)
    data.id = request_id
    data.status = StatusEnum.PENDING
    await collection.insert_one(data.dict())  # type: ignore
    await db_connect.close_db()
    request = await get_request(request_id)  # type: ignore
    return request


async def get_next_request_id(counter, collection_name):
    """
    This method generates the sequence id for the MongoDB document
    """
    db_connect = DBConnect()
    await _check_collection_counter()
    collection = await db_connect.get_collection(name=counter)
    document = await collection.find_one({"_id": collection_name})  # type: ignore
    collection.update_one({"_id": collection_name}, {"$inc": {"value": 1}})  # type: ignore
    await db_connect.close_db()
    return f"REQ:{(document['value'] + 1):07}"


async def update_request(
    request_id: str, data: Union[Request, RequestPartial]
) -> Request:
    """
    update a request
    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(name=COLLECTION_NAME)
    if data.status == StatusEnum.REJECTED or data.status == StatusEnum.APPROVED:
        collection.update_one(  # type: ignore
            {"id": request_id}, {"$set": data.dict(exclude_unset=True)}
        )
    await db_connect.close_db()
    request = await get_request(request_id)  # type: ignore
    return request


async def delete_request(request_id: str):
    """
    delete a request
    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(name=COLLECTION_NAME)
    collection.delete_one({"id": request_id})  # type: ignore
    await db_connect.close_db()


async def _check_collection_counter():
    """
    Check whether counter for collection 'requests' exists.
    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(name=COUNTER)
    docs = await collection.find().to_list(None)
    if len(docs) == 0:
        await _initialize_collection_counter()


async def _initialize_collection_counter():
    """
    Initialize a counter for collection 'requests'.
    """
    db_connect = DBConnect()
    collection = await db_connect.get_collection(name=COUNTER)
    collection.insert_one({"_id": COLLECTION_NAME, "value": 0})
