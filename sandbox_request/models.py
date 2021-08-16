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


"""Defines all dataclasses/classes pertaining to a data model or schema"""

from typing import Optional
from pydantic import BaseModel


class Request(BaseModel):
    """
    Class Request
    """

    _id: str
    dataset_id: str
    purpose: str
    request_id: str
    status: str
    user_id: str


class RequestPartial(BaseModel):
    """
    Class Request for partial updates (PATCH).
    Only a subset of attributes of Request can
    be modified.
    """

    purpose: Optional[str] = None
    request_id: str
    status: Optional[str] = None
