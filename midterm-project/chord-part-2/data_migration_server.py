from fastapi import FastAPI
from http import HTTPStatus
import hashlib
import requests
from os import listdir
from pydantic import BaseModel
import msgpackrpc
from ec2_metadata import ec2_metadata
import time


class Node(BaseModel):
    id: int
    ip: str
    port: int


def hash(str):
    return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)


def new_client(ip, port):
    return msgpackrpc.Client(msgpackrpc.Address(ip, port))


def get_info(ip):
    client = new_client(ip, 5057)
    node = client.call("get_info")
    return node


def get_file_owner_ip(ip, file_name):
    h = hash(file_name)
    client = new_client(ip, 5057)
    file_onwer = client.call("find_successor", h)
    print("get file {} onwer.".format(file_name))
    return file_onwer[0].decode()


app = FastAPI()


@app.post("/notify_join_system", status_code=HTTPStatus.OK)
async def upload_file_to_predecessor(predecessor: Node):
    source_path = '/home/ec2-user/files/'

    files_to_upload = []

    for f in listdir(source_path):
        file_owner_ip = get_file_owner_ip(ec2_metadata.public_ipv4, f)
        print("file_owner_ip: ", file_owner_ip)
        if file_owner_ip == predecessor.ip:
            files_to_upload.append(f)

    for f in files_to_upload:
        files = {
            'files': open(source_path + f, 'rb'),
        }
        print("Uploading file to http://{}".format(predecessor.ip))
        requests.post(
            'http://{}:5058/upload'.format(predecessor.ip), files=files)

    return {"files": files_to_upload}
