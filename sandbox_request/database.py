"""
    Module database.py
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

import motor.motor_asyncio

DB_URL = "mongodb://localhost:27017"
DB_NAME = "sandbox_requests_db"


class Database:
    """
    class Database
    """

    def __init__(self) -> None:
        self.client = motor.motor_asyncio.AsyncIOMotorClient()

    async def get_db(self):
        """
        Return database client instance.
        """
        self.client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
        return self.client

    async def close_db(self):
        """
        Close database connection.
        """
        self.client.close()

    async def get_collection(self, name) -> object:
        """
        Get a collection
        """
        client = await self.get_db()
        collection = client[DB_NAME][name]
        return collection
