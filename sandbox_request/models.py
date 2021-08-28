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
This module contains Pydantic models used by the Request Service API.
"""

from typing import Optional
from enum import Enum
from pydantic import BaseModel


class StatusEnum(str, Enum):
    """
    Class StatusEnum for enumerating the possible statuses
    """

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Request(BaseModel):
    """
    Class Request
    """

    dataset_id: str
    purpose: str
    id: Optional[str] = None
    status: StatusEnum
    user_id: str

    class Config:
        """
        Class config to allow the usage of Enum for Status in Request class
        """

        use_enum_values = True


class RequestPartial(BaseModel):
    """
    Class Request for partial updates (PATCH).
    Only a subset of attributes of Request can
    be modified.
    """

    purpose: Optional[str] = None
    status: StatusEnum

    class Config:
        """
        Class config to allow the usage of Enum for Status in Request class
        """

        use_enum_values = True
