import hashlib
import json
import os
import pickle
from typing import Any, Iterable
from uuid import uuid4

from pydantic import BaseModel
import requests

from flask import Flask, request, Response
from imagination.standalone import container
from imagination.decorator.service import Service
from opentelemetry import trace

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

tracer = trace.get_tracer("s1")
app = Flask(__name__)


class ObjectMetadata(BaseModel):
    id: str


class Bucket:
    def __init__(self, name: str, path: str):
        self._name = name
        self._path = path

        print(f'Storage/{self._name} @ {self._path}')
        if not os.path.exists(self._path):
            os.makedirs(self._path, exist_ok=True)

    def list(self) -> Iterable[ObjectMetadata]:
        for i in os.listdir(self._path):
            yield ObjectMetadata(id=i)

    def get(self, id: str) -> Any:
        with open(os.path.join(self._path, id), 'rb') as f:
            return pickle.load(f)

    def set(self, id: str, data: Any) -> ObjectMetadata:
        with open(os.path.join(self._path, id), 'wb') as f:
            return pickle.dump(data, f)

    def set_quick(self, data: Any) -> ObjectMetadata:
        id = str(uuid4())
        with open(os.path.join(self._path, id), 'wb') as f:
            pickle.dump(data, f)
        return ObjectMetadata(id=id)


@Service()
class Storage:
    def __init__(self):
        print(f'Storage @ {DATA_DIR}')
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR, exist_ok=True)

    def bucket(self, name: str) -> Bucket:
        return Bucket(name, os.path.join(DATA_DIR, self._encode_bucket_name(name)))

    @staticmethod
    def _encode_bucket_name(name: str):
        h = hashlib.new('sha1')
        h.update(name.encode('utf-8'))
        return h.hexdigest()


class NoticeRequest(BaseModel):
    title: str
    content: str


@app.route("/api/notices", methods=['GET'])
def list_notices():
    storage: Storage = container.get(Storage)

    if True:  # with tracer.start_as_current_span("ping.begin") as span:
        requests.get(f'http://localhost:8081/ping/notices/list-all/begin')

    with tracer.start_as_current_span("storage.bucket.list") as span:
        span.set_attribute('bucket', 'notices')
        items = storage.bucket('notices').list()

    if True:  # with tracer.start_as_current_span("ping.begin") as span:
        requests.get(f'http://localhost:8081/ping/notices/list-all/end')

    with tracer.start_as_current_span("http.api.serialize_response") as span:
        return Response(json.dumps([i.dict() for i in items]),
                        status=200,
                        content_type='application/json')


@app.route("/api/notices", methods=['POST'])
def post_new_notice():
    storage: Storage = container.get(Storage)

    if True:  # with tracer.start_as_current_span("ping.begin") as span:
        requests.get(f'http://localhost:8081/ping/notices/post-new/begin')

    with tracer.start_as_current_span("storage.bucket.set") as span:
        span.set_attribute('bucket', 'notices')
        obj_metadata = storage.bucket('notices').set_quick(NoticeRequest(**request.json).dict())
        span.set_attribute('object.id', obj_metadata.id)

    if True:  # with tracer.start_as_current_span("ping.begin") as span:
        requests.get(f'http://localhost:8081/ping/notices/post-new/end')

    with tracer.start_as_current_span("http.api.serialize_response") as span:
        return Response(obj_metadata.json(),
                        status=200,
                        content_type='application/json')


@app.route("/api/notices/<string:id>", methods=['GET'])
def get_notice(id: str):
    storage: Storage = container.get(Storage)

    if True:  # with tracer.start_as_current_span("ping.begin") as span:
        requests.get(f'http://localhost:8081/ping/notices/get-{id}/begin')

    with tracer.start_as_current_span("storage.bucket.set") as span:
        span.set_attribute('bucket', 'notices')
        span.set_attribute('object.id', id)
        data = storage.bucket('notices').get(id)

    if True:  # with tracer.start_as_current_span("ping.begin") as span:
        requests.get(f'http://localhost:8081/ping/notices/get-{id}/end')

    with tracer.start_as_current_span("http.api.serialize_response") as span:
        return Response(json.dumps(data),
                        status=200,
                        content_type='application/json')
