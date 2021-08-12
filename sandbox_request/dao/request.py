"""
    Module request.py
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


from typing import Dict
from sandbox_request.database import Database
from sandbox_request.channels import send_mail

COLLECTION_NAME = "requests"


async def get_all_requests() -> object:
    """
    get list of all requests

    Returns:
        object:
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    requests = collection.find()  # type: ignore
    return await requests.to_list(None)


async def get_request(request_id):
    """
    get request
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    request = await collection.find_one({"id": request_id})  # type: ignore
    return request


async def add_request(data: Dict):
    """
    add new request
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    request_id = data["id"]
    await collection.insert_one(data)  # type: ignore
    dataset = await get_request(request_id)
    send_mail("data_steward", "request_made")
    return dataset


async def update_request(request_id: str, data: dict):
    """
    update a request
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    collection.update_one({"id": request_id}, {"$set": data})  # type: ignore
    return await collection.find_one({"id": request_id})  # type: ignore


async def delete_request(request_id: str):
    """
    delete a request
    """
    database = Database()
    collection = await database.get_collection(name=COLLECTION_NAME)
    collection.delete_one({"id": request_id})  # type: ignore
