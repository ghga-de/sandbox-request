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

DB_NAME = "sandbox_request_db"
REQUESTS = "requests"
COUNTER = "counter"
COUNTER_JSON = {"_id": "requests", "value": 0}


async def insert_records(db_name, collection_name, records):
    """
    insert requests
    """
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[db_name][collection_name]
    await collection.insert_many(records)


async def insert_one(db_name, collection_name, document):
    """
    insert counter
    """
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[db_name][collection_name]
    await collection.insert_one(document)


async def delete_all_records(db_name, collection_name):
    """
    delete requests
    """
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[db_name][collection_name]
    await collection.delete_many({})


async def update_counter(db_name, counter, collection_name):
    """
    This method generates the sequence id for the MongoDB document
    """
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[db_name][counter]
    collection.update_one({"_id": collection_name}, {"$inc": {"value": 1}})  # type: ignore


async def get_collection(db_name, collection_name):
    """
    get all requests
    """
    client = motor.motor_asyncio.AsyncIOMotorClient()
    collection = client[db_name][collection_name]
    result = collection.find()
    return await result.to_list(None)


with open("examples/requests.json") as request_file:
    file_records = json.load(request_file)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_all_records(DB_NAME, REQUESTS))
    loop.run_until_complete(delete_all_records(DB_NAME, COUNTER))
    loop.run_until_complete(insert_one(DB_NAME, COUNTER, COUNTER_JSON))
    for record in file_records[REQUESTS]:
        loop.run_until_complete(insert_one(DB_NAME, REQUESTS, record))
        loop.run_until_complete(update_counter(DB_NAME, COUNTER, REQUESTS))
    print(loop.run_until_complete(get_collection(DB_NAME, REQUESTS)))
    print(loop.run_until_complete(get_collection(DB_NAME, COUNTER)))
