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
This module define the API endpoints that collectively
form the Request Service API.
"""

from fastapi import FastAPI
from ghga_service_chassis_lib.api import configure_app

from sandbox_request.config import get_config
from sandbox_request.dao.db_connect import DBConnect
from sandbox_request.routes.requests import request_router

CONFIG = get_config()
app = FastAPI(
    title="Request Service API",
    root_path=CONFIG.fastapi_options["root_path"],
    openapi_url=CONFIG.fastapi_options["openapi_url"],
    docs_url=CONFIG.fastapi_options["docs_url"],
)
configure_app(app, config=CONFIG)
db_connect = DBConnect()

app.include_router(request_router)
app.add_event_handler("startup", db_connect.get_db)
app.add_event_handler("shutdown", db_connect.close_db)
