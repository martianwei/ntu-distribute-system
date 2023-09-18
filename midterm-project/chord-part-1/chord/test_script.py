#!/usr/bin/python3

import msgpackrpc
import time
import sys

clientCnt = int(sys.argv[1])

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))
clinetArr = []
for i in range(5057 , 5057 + clientCnt):
	clinetArr.append(new_client("127.0.0.1", i))

for c in clinetArr:
	print(c.call("get_info"))

for i in range(0 , clientCnt):
	print(i)
	if(i == 0):
		clinetArr[i].call("create")
		continue
	time.sleep(2)
	clinetArr[i].call("join", clinetArr[0].call("get_info"))

# test the functionality after all nodes have joined the Chord ring

time.sleep(20)
print(clinetArr[2].call("find_successor", 3072633950))

time.sleep(2)
print(clinetArr[1].call("find_successor", 3072633950))

time.sleep(2)
clinetArr[1].call("kill")
clinetArr[0].call("kill")

time.sleep(40)
print(clinetArr[2].call("find_successor", 3072633950))

time.sleep(2)
print(clinetArr[3].call("find_successor", 3072633950))




