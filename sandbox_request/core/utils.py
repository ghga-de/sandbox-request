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
All core utilities for the functionality of Request Service API.
"""

from typing import Dict, Optional
import requests
from fastapi import HTTPException
from sandbox_request.config import get_config


async def check_dataset(dataset_id: str) -> Optional[Dict]:
    """Check if the given dataset ID exists in the metadata store."""
    config = get_config()
    dataset = None
    url = f"{config.svc_metadata_url}/datasets/{dataset_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dataset = response.json()
        elif response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset {dataset_id} could not be found in the metadata store. "
                + "Cannot create a request for a dataset that does not exist.",
            )
        else:
            response.raise_for_status()
    except requests.RequestException as ex:
        raise HTTPException(status_code=502, detail=ex.errno) from ex
    return dataset
