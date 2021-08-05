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

FROM python:3.9.6-buster

COPY . /service
WORKDIR /service
RUN pip install -r requirements.txt

# create new user and execute as that user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "sandbox_request.api:app"]
