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
Entrypoint of the package
"""

from ghga_service_chassis_lib.api import run_server
import typer
from sandbox_request.config import get_config
from sandbox_request.api import app  # noqa: F401 pylint: disable=unused-import
from sandbox_request.pubsub import subscribe


cli = typer.Typer()


@cli.command()
def rest_api():
    """Serve the RESTful API"""
    run_server(app="sandbox_request.__main__:app", config=get_config())


@cli.command()
def async_api():
    """Run a process that subscribes to relevant async topics."""
    subscribe()


if __name__ == "__main__":
    cli()
