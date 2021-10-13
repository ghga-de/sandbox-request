#!/usr/bin/env python3

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
    Populate the database with example data.
"""

import asyncio
import json
from pathlib import Path

import motor.motor_asyncio
import typer

HERE = Path(__file__).parent.resolve()

DEFAULT_EXAMPLES_DIR = HERE.parent.resolve() / "examples"
DEFAULT_DB_URL = "mongodb://db:27017"
DEFAULT_DB_NAME = "request"

REQUESTS = "requests"
COUNTER = "counter"
COUNTER_JSON = {"_id": "requests", "value": 0}


async def insert_one(db_url: str, db_name: str, collection_name: str, document: dict):
    """
    insert counter
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    collection = client[db_name][collection_name]
    await collection.insert_one(document)


async def delete_all_records(db_url: str, db_name: str, collection_name: str):
    """
    delete requests
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    collection = client[db_name][collection_name]
    await collection.delete_many({})


async def update_counter(db_url: str, db_name: str, counter: str, collection_name: str):
    """
    This method generates the sequence id for the MongoDB document
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    collection = client[db_name][counter]
    collection.update_one({"_id": collection_name}, {"$inc": {"value": 1}})  # type: ignore


async def get_collection(db_url: str, db_name: str, collection_name: str):
    """
    get all requests
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    collection = client[db_name][collection_name]
    result = collection.find()
    return await result.to_list(None)


async def reset_and_populate_db(
    db_url: str, db_name: str, example_dir: Path = DEFAULT_EXAMPLES_DIR
):
    """
    Deletes all DB entries and populates the
    database with examples
    """

    with open(example_dir / "requests.json") as requests_file:
        requests = json.load(requests_file)

    # reset/populate the COUNTER collection:
    await delete_all_records(db_url, db_name, COUNTER)
    await insert_one(db_url, db_name, COUNTER, COUNTER_JSON)

    # reset/populate the COUNTER collection:
    await delete_all_records(db_url, db_name, REQUESTS)
    for request in requests:
        await insert_one(db_url, db_name, REQUESTS, request)
        await update_counter(db_url, db_name, COUNTER, REQUESTS)
    typer.echo("- added Counter:")
    typer.echo(await get_collection(db_url, db_name, COUNTER))
    typer.echo("- added Requests:")
    typer.echo(await get_collection(db_url, db_name, REQUESTS))


def main(
    db_url: str = DEFAULT_DB_URL,
    db_name: str = DEFAULT_DB_NAME,
    example_dir: Path = DEFAULT_EXAMPLES_DIR,
):
    """Main entrypoint. Handles the event loop."""

    typer.echo("This will populate the database with examples.")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(reset_and_populate_db(db_url, db_name, example_dir))

    typer.echo("Done.")


if __name__ == "__main__":
    typer.run(main)
