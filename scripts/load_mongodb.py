"""
    Module load_mongodb.py
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

import asyncio
import json
import motor.motor_asyncio


async def insert_records(db_name, collection_name, records):
    """
    insert requests
    """
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[db_name][collection_name]
    await collection.insert_many(records)


async def delete_all_records(db_name, collection_name):
    """
    delete requests
    """
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[db_name][collection_name]
    await collection.delete_many({})


async def get_collection(db_name, collection_name):
    """
    get all requests
    """
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[db_name][collection_name]
    result = collection.find()
    return await result.to_list(None)


DB_NAME = "sandbox_requests_db"

with open("examples/requests.json") as file:
    file_records = json.load(file)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_all_records(DB_NAME, "requests"))
    loop.run_until_complete(
        insert_records(DB_NAME, "requests", file_records["requests"])
    )
    print(loop.run_until_complete(get_collection(DB_NAME, "requests")))
