# sandbox-request

This is the microservice that handles incoming requests from Data requester for accessing the 
mmetadata and the files. The requests are forwarded to the relevant Data stewards and DAC. The request calls are almost always Asynchronous calls.

To run the application

    cd sandbox-request
    docker build -t sandbox-request . 
    docker run -d -p 8000:8000 sandbox-request
To run unit test

    cd test
    pytest "filename".py
alternatively to run all tests at once

    pytest *.py