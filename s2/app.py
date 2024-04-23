import asyncio
from random import randint

from fastapi import FastAPI
from opentelemetry import trace

tracer = trace.get_tracer("s2")
app = FastAPI()


@app.get("/ping/{bucket}/{id}/{action}")
async def ping(bucket: str, id: str, action: str):
    delay = 1 if action == 'begin' else randint(1, 5)
    await asyncio.sleep(delay)
    return {"bucket": bucket, "id": id, "action": action, "delay": delay}
