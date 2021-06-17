FROM sanicframework/sanic:LTS

WORKDIR /service

COPY . /service

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "./sandbox_request/app.py"]
