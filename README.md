**Depreciation Note:   
Please note, this repo was part of an implementation study and is not longer maintained.
Please do not use for production.** 

---

# Sandbox Request Service

Sandbox request acts as a communication platform for Data Requesters, Data Stewards, and DAC Representatives to negotiate on a request to access a specific dataset. This service pulls in every request-relevant event and persists an event history for each request..


## Setting up the dev environment

A `Dockerfile` (and `docker-compose.yaml`) for a container corresponding to a development environment has been configured and made available in the `.devcontainer` folder.

You can use the configurations in `.devcontainer` to run VS Code in a Docker container via the [Remote Container extension for VS Code](https://code.visualstudio.com/docs/remote/containers-tutorial).

Alternatively, you can also run the container directly from your command line as follows:

```sh
# build the image first
docker build -t sandbox-request:dev -f .devcontainer/Dockerfile .

# run the container
docker run --rm -it -u vscode -v "${PWD}:/workspace" sandbox-request:dev bash
```


## Running the application

You can run the application in two ways,

```sh
sandbox-request
```

or,

```sh
uvicorn sandbox_request.main:app --reload
```

You can visit the API by navigating to [http://localhost:8000/docs]()


## Bootstrapping the database for the application

The request service relies on a MongoDB instance that keeps track of requests and their approval status.

All request records are stored in the `requests` collection.

To pre-load request records into a fresh instance of MongoDB:

```sh
# load request records
python scripts/populate_request_store.py --base-url http://localhost:8000 --directory examples
```
