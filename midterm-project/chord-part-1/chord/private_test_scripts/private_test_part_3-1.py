#!/usr/bin/python3

import msgpackrpc
import time

ids = []
find_successor_req = 0
incorrect = 0
t = 2

def add_id(id):
	if id not in ids:
		ids.append(id)
		ids.sort()

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def get_id(port):
	client = new_client("127.0.0.1", port)
	return client.call("get_info")[2]

def create(port):
	client = new_client("127.0.0.1", port)
	client.call("create")
	add_id(get_id(port))
	print("node {} created a chord ring".format(port))

def join(port1, port2):
	client1 = new_client("127.0.0.1", port1)
	client2 = new_client("127.0.0.1", port2)
	client1.call("join", client2.call("get_info"))
	add_id(get_id(port1))
	print("node {} joined node {}".format(port1, port2))

def kill(port):
	id = get_id(port)
	ids.remove(id)
	client = new_client("127.0.0.1", port)
	client.call("kill")
	print("node {} killed".format(port))

def get_ans(id):
	if id > ids[-1]:
		return ids[0]
	i = 0
	while ids[i] < id:
		i += 1
	return ids[i]

def find_successor(port, id):
	client = new_client("127.0.0.1", port)
	return client.call("find_successor", id)[2]

def verify(port, id):
	global find_successor_req, incorrect
	find_successor_req += 1
	get = find_successor(port, id)
	if get == get_ans(id):
		print("find_successor({}, {}) correct.".format(port, id))
	else:
		print("find_successor({}, {}) incorrect, ans: {}, get: {}.".format(port, id, get_ans(id), get))
		incorrect += 1

def wait(t):
	print("wait {} sec...".format(t))
	time.sleep(t)

create(5065)
wait(t)

join(5066, 5065)
wait(t)
join(5067, 5066)
wait(t)
join(5068, 5067)
wait(10 * t)

kill(5065)
wait(10 * t)
kill(5066)
wait(20 * t)

join(5069, 5068)
wait(t)
join(5070, 5069)
wait(t)
join(5071, 5070)
wait(t)
join(5072, 5071)
wait(t)
join(5073, 5072)
wait(t)
join(5074, 5073)
wait(t)
join(5075, 5074)
wait(t)
join(5076, 5075)
wait(t)
join(5077, 5076)
wait(t)
join(5078, 5077)
wait(t)
join(5079, 5078)
wait(t)
join(5080, 5079)
wait(10 * t)

kill(5076)
wait(10 * t)
kill(5075)
wait(10 * t)
kill(5074)
wait(20 * t)

testcases = [1, 20000000, 70000000, 120000000, 1330000000, 1440000000, 1560000000, 1650000000, 2000000000, 2100000000, 2200000000, 3000000000, 3131313131, 3737373737, 3838383838, 3939393939, 4080500002]

for case in testcases:
	id = case

	for port in [5067, 5068, 5069, 5070, 5071, 5072, 5073, 5077, 5078, 5079, 5080]:
		verify(port, id)
		wait(t)

print("{} find successor requests, ".format(find_successor_req), end="")
if (incorrect == 0):
	print("All correct.")
else:
	print("{} incorrect response(s).".format(incorrect))

print("Do not forget to terminate your Chord nodes!")
