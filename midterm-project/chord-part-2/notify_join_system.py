import msgpackrpc
import requests
import time
from ec2_metadata import ec2_metadata


def new_client(ip, port):
    return msgpackrpc.Client(msgpackrpc.Address(ip, port))


def get_successor(ip, idx):
    client = new_client(ip, 5057)
    successor = client.call("get_successor", idx)
    print("get node {}:{} {} successor.".format(ip, 5057, idx))
    return successor


def get_info(ip):
    client = new_client(ip, 5057)
    return client.call("get_info")


time.sleep(20)

mynode = get_info(ec2_metadata.public_ipv4)
successor = get_successor(ec2_metadata.public_ipv4, 0)
successor_ip = successor[0].decode()
print("successor: ", successor)
node = {
    'ip': mynode[0].decode(),
    'port': mynode[1],
    'id': mynode[2]
}
print('http://{}:5059/notify_join_system"'.format(successor_ip))
print("node: ", node)
response = requests.post(
    'http://{}:5059/notify_join_system'.format(successor[0].decode()), json=node)

print(response.content)
