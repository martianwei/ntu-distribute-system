#!/usr/bin/python3

import sys
import requests
import msgpackrpc
import hashlib

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def hash(str):
	return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)

output_file_name = sys.argv[1]
ip = sys.argv[2]

client = new_client(ip, 5057)


chunk_num = 1
with open(output_file_name, 'wb') as f:
	while True:
		chunk_file_name = output_file_name + '_chunk_' + str(chunk_num)
		h = hash(chunk_file_name)
		print("Hash of {} is {}".format(chunk_file_name, h))
		node = client.call("find_successor", h)
		node_ip = node[0].decode()
		print("Downloading file from http://{}".format(node_ip))
		response = requests.get("http://{}:5058/{}".format(node_ip, chunk_file_name))
		print(response)
		if(response.status_code != 200):
			break
		f.write(response.content)
		chunk_num += 1
