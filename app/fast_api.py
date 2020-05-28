"fast_api.py - Simple API to expose DB data"
from typing import List
from datetime import datetime

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from app.database import transactions

app = FastAPI()

class Activity(BaseModel):
    start_of_activity: str
    end_of_activity: str

class Node(BaseModel):
    user_agent: str = None
    active: bool
    highest_protocol: str
    services: List[str] = []
    activities: List[Activity] = []
    port: int

class Address(BaseModel):
    ip: str
    port: int
    last_seen: datetime = None
    inserted: datetime = None
    node_assign: bool


@app.get("/node/{ip_address_with_port}", response_model=Node)
async def get_node(ip_address_with_port: str):
    ip_and_port = ip_address_with_port.rsplit(":", 1)
    try:
        ip = ip_and_port[0].replace("]","").replace("[","")
        port = ip_and_port[1]
    except IndexError:
        raise HTTPException(400, "Node address is invalid")
    found_node = transactions.find_node(ip, port)
    if not found_node:
        raise HTTPException(404, "Node not found")
    return found_node


@app.get("/nodes/{ip_address}", response_model=List[Node])
async def get_nodes(ip_address: str):
    ip = ip_address.replace("]","").replace("[","")
    found_nodes = transactions.find_nodes(ip)
    if not found_nodes:
        raise HTTPException(404, "Nodes not found")
    return transactions.find_nodes(ip)


@app.get("/address/{ip_address_with_port}", response_model=Address)
async def get_address(ip_address_with_port: str):
    ip_and_port = ip_address_with_port.rsplit(":", 1)
    try:
        ip = ip_and_port[0].replace("]","").replace("[","")
        port = ip_and_port[1]
    except IndexError:
        raise HTTPException(400, "Node address is invalid")
    found_address = transactions.find_address(ip, port)
    if not found_address:
        raise HTTPException(404, "Node not found")
    return found_address
