#!/usr/bin/python3

import sys
import requests
import msgpackrpc
import hashlib
import io


def new_client(ip, port):
    return msgpackrpc.Client(msgpackrpc.Address(ip, port))


def hash(str):
    return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)


filename = sys.argv[1]
ip = sys.argv[2]

filepath = filename
slashs = [i for i, c in list(enumerate(filepath)) if c == '/']
if len(slashs) != 0:
    filename = filename[max(slashs) + 1:]

print("filename: ", filename)
client = new_client(ip, 5057)

chunk_size = 4000  # 4KB

# for i in range(1, 20):
with open(filepath, 'rb') as f:
    chunk_num = 1
    while True:
        # chunk_stream = io.BytesIO()
        chunk_data = f.read(chunk_size)
        if not chunk_data:
            break
        chunk_file_name = '{}_chunk_{}'.format(filename, chunk_num)
        h = hash(chunk_file_name)
        print("Hash of {} is {}".format(chunk_file_name, h))
        node = client.call("find_successor", h)
        node_ip = node[0].decode()
        chunk_stream = io.BytesIO(chunk_data)
        chunk_stream.name = chunk_file_name
        files = {
            'files': io.BufferedReader(chunk_stream),
        }
        print(files)
        print("Uploading file to http://{}".format(node_ip))
        response = requests.post(
            'http://{}:5058/upload'.format(node_ip), files=files)
        chunk_num += 1
