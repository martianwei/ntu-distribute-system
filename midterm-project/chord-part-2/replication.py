import requests
from os import listdir
from ec2_metadata import ec2_metadata
import time
import msgpackrpc
import hashlib


class Neighbor:
    def __init__(self, predecessor_ip: str, first_successor_ip: str, second_successor_ip: str):
        self.predecessor_ip = predecessor_ip
        self.first_successor_ip = first_successor_ip
        self.second_successor_ip = second_successor_ip


def hash(str):
    return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)


def new_client(ip, port):
    return msgpackrpc.Client(msgpackrpc.Address(ip, port))


def get_predecessor_ip(ip):
    client = new_client(ip, 5057)
    predecessor = client.call("get_predecessor")
    print("get node {}:{} predecessor.".format(ip, 5057))
    return predecessor[0].decode()


def get_successor_ip(ip, idx):
    client = new_client(ip, 5057)
    successor = client.call("get_successor", idx)
    print("get node {}:{} {} successor.".format(ip, 5057, idx))
    return successor[0].decode()


def get_file_owner_ip(ip, file_name):
    h = hash(file_name)
    client = new_client(ip, 5057)
    file_onwer = client.call("find_successor", h)
    print("get file {} onwer.".format(file_name))
    return file_onwer[0].decode()


def check_neighbor_same():
    global neighbor
    print("check_neighbor_same")
    new_predecessor_ip = get_predecessor_ip(ec2_metadata.public_ipv4)
    new_first_successor_ip = get_successor_ip(ec2_metadata.public_ipv4, 0)
    new_second_successor_ip = get_successor_ip(ec2_metadata.public_ipv4, 1)
    alive = ((neighbor.predecessor_ip == new_predecessor_ip) & (neighbor.first_successor_ip ==
             new_first_successor_ip) & (neighbor.second_successor_ip == new_second_successor_ip))
    neighbor.predecessor_ip = new_predecessor_ip
    neighbor.first_successor_ip = new_first_successor_ip
    neighbor.second_successor_ip = new_second_successor_ip
    return alive


def replication(neighbor_same: bool):
    global old_files_set_size
    global files_set
    source_path = '/home/ec2-user/files/'
    files = [f for f in listdir(source_path)]
    print("old_files_set_size: ", old_files_set_size)
    print("new_files_set_size: ", len(files))
    need_check_files = []
    if (len(files) == old_files_set_size) & neighbor_same:
        return
    elif neighbor_same:
        need_check_files = [f for f in files if f not in files_set]
    else:
        need_check_files = files

    for f in need_check_files:
        files_set.add(f)
        file_owner_ip = get_file_owner_ip(ec2_metadata.public_ipv4, f)
        print("file_owner_ip: ", file_owner_ip)
        if file_owner_ip == ec2_metadata.public_ipv4:
            files = {
                'files': open(source_path + f, 'rb'),
            }

            response = requests.get(
                "http://{}:5058/{}".format(neighbor.first_successor_ip, f))
            if (response.status_code != 200):
                print("Uploading file to http://{}".format(neighbor.first_successor_ip))
                requests.post(
                    'http://{}:5058/upload'.format(neighbor.first_successor_ip), files=files)
            response = requests.get(
                "http://{}:5058/{}".format(neighbor.second_successor_ip, f))
            if (response.status_code != 200):
                print("Uploading file to http://{}".format(neighbor.second_successor_ip))
                requests.post(
                    'http://{}:5058/upload'.format(neighbor.second_successor_ip), files=files)
    old_files_set_size = len(files_set)


files_set = set()
old_files_set_size = 0
neighbor = Neighbor(predecessor_ip='', first_successor_ip='',
                    second_successor_ip='')
while True:
    time.sleep(8)
    print("start replication")
    neighbor_same = check_neighbor_same()
    replication(neighbor_same)
