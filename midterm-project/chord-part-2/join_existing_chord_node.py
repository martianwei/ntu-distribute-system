import boto3
import msgpackrpc
import logging
import time
from ec2_metadata import ec2_metadata
from botocore.exceptions import ClientError
import os
print("join_existing_chord_node start")
logger = logging.getLogger(__name__)


def new_client(ip, port):
    return msgpackrpc.Client(msgpackrpc.Address(ip, port))


def create(ip):
    client = new_client(ip, 5057)
    client.call("create")
    print("node {}:{} created a chord ring".format(ip, 5057))


def join(ip1, ip2):
    client1 = new_client(ip1, 5057)
    client2 = new_client(ip2, 5057)
    node = client2.call("get_info")
    client1.call("join", node)
    print("node {}:{} joined node {}:{}".format(ip1, 5057, ip2, 5057))


class AutoScalingWrapper:
    def __init__(self, autoscaling_client):
        self.autoscaling_client = autoscaling_client

    def getAutoScalingGroupInstanceIDs(self, group_name):
        try:
            response = self.autoscaling_client.describe_auto_scaling_groups(
                AutoScalingGroupNames=[group_name])
        except ClientError as err:
            logger.error(
                "Couldn't describe group %s. Here's why: %s: %s", group_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            instanceIDs = [x["InstanceId"]
                           for x in response["AutoScalingGroups"][0]["Instances"]]
            return instanceIDs


def getPublicIP(instanceID):
    ec2 = boto3.client('ec2', region_name='us-east-1')
    publicIP = ec2.describe_instances(
        InstanceIds=[instanceID,],
    )['Reservations'][0]['Instances'][0]['PublicIpAddress']
    return publicIP


autoscalingClient = boto3.client('autoscaling', region_name='us-east-1')
autoScalingWrapper = AutoScalingWrapper(autoscalingClient)
exist_instanceIDs = autoScalingWrapper.getAutoScalingGroupInstanceIDs(
    "MyChordFileSystemASG")
print("instanceIDs: ", exist_instanceIDs)

# Start Chord node
os.system("/home/ec2-user/scripts/chord {} 5057 &".format(ec2_metadata.public_ipv4))
print("Chord Node start listen in {}:5057".format(ec2_metadata.public_ipv4))
time.sleep(5)
# Join existing Chord system
if len(exist_instanceIDs) == 1:
    create(ec2_metadata.public_ipv4)
else:
    if getPublicIP(exist_instanceIDs[0]) == ec2_metadata.public_ipv4:
        join(ec2_metadata.public_ipv4, getPublicIP(exist_instanceIDs[1]))
    else:
        join(ec2_metadata.public_ipv4, getPublicIP(exist_instanceIDs[0]))
