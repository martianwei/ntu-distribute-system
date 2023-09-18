import boto3
from ec2_metadata import ec2_metadata
from botocore.exceptions import ClientError
import logging
import time
logger = logging.getLogger(__name__)


class CloudWatchWrapper:
    def __init__(self, cloudwatch_resource):
        self.cloudwatch_resource = cloudwatch_resource

    def list_metrics(self, namespace, name, instance_id, recent=False):
        try:
            kwargs = {'Namespace': namespace, 'MetricName': name, 'Dimensions': [
                {'Name': 'InstanceId', 'Value': instance_id}]}
            if recent:
                kwargs['RecentlyActive'] = 'PT3H'  # List past 3 hours only
            metric_iter = self.cloudwatch_resource.metrics.filter(**kwargs)
            logger.info("Got metrics for %s.%s.", namespace, name)
        except ClientError:
            logger.exception(
                "Couldn't get metrics for %s.%s.", namespace, name)
            raise
        else:
            return metric_iter


class AutoScalingWrapper():
    def __init__(self, autoScaling_client):
        self.autoScaling_client = autoScaling_client

    def getAutoScalingGroupInstanceIDs(self, group_name):
        try:
            response = self.autoScaling_client.describe_auto_scaling_groups(
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

    def put_scaling_policy(self, autoScaling_group_name, policy_name, adjustment_type="ChangeInCapacity", scaling_adjustment=1, cooldown=180):
        try:
            kwargs = {'AutoScalingGroupName': autoScaling_group_name,
                      'PolicyName': policy_name,
                      'AdjustmentType': adjustment_type,
                      'ScalingAdjustment': scaling_adjustment,
                      'Cooldown': cooldown,
                      }
            policy = self.autoScaling_client.put_scaling_policy(**kwargs)
            logger.info(
                "Added scaling_policy %s to autoScaling_group %s.", policy_name, autoScaling_group_name,
            )
        except ClientError:
            logger.exception(
                "Couldn't add scaling_policy %s to autoScaling_group %s.", policy_name, autoScaling_group_name)
            raise
        else:
            return policy


# Create CloudWatchWrapper
cloudwatchClient = boto3.client('cloudwatch', region_name='us-east-1')
cloudwatchResource = boto3.resource('cloudwatch', region_name='us-east-1')
cloudWatchWrapper = CloudWatchWrapper(cloudwatchResource)

# Create Autoscaling Client
autoscalingClient = boto3.client('autoscaling', region_name='us-east-1')
autoscalingWrapper = AutoScalingWrapper(autoscalingClient)

policy = autoscalingWrapper.put_scaling_policy(
    "MyChordFileSystemASG", "disk_used_persent")
print(policy)


exist_instanceIDs = autoscalingWrapper.getAutoScalingGroupInstanceIDs(
    "MyChordFileSystemASG")
print("instanceIDs: ", exist_instanceIDs)


metric_querys = []
for i in range(len(exist_instanceIDs)):
    metric_querys.append(
        {
            "Id": f'm_{i}',
            "MetricStat": {
                "Metric": {
                    "Namespace": "CWAgent",
                    "MetricName": "disk_used_percent",
                    "Dimensions": [
                        {
                            'Name': 'AutoScalingGroupName',
                            'Value': 'MyChordFileSystemASG'
                        },
                        {
                            "Name": "InstanceId",
                            "Value": exist_instanceIDs[i]
                        },
                        {
                            'Name': 'device',
                            'Value': 'xvda1'
                        },
                        {
                            'Name': 'fstype',
                            'Value': 'xfs'
                        },
                        {
                            'Name': 'path',
                            'Value': '/'
                        },
                    ]
                },
                "Period": 60,
                "Stat": "Average",
                "Unit": "Percent"
            },
            "ReturnData": False
        }
    )
expression_querys = [{
    'Id': 'expr_1',
    'Expression': 'AVG(METRICS())',
    'ReturnData': True
}]


metrics = metric_querys + expression_querys
print("metrics: ", metrics)
tryCnt = 0
while (True):
    list_metrics_result = list(cloudWatchWrapper.list_metrics(
        "CWAgent", "disk_used_percent", ec2_metadata.instance_id))
    if len(list_metrics_result) == 0:
        tryCnt += 1
        print("tryCnt: ", tryCnt)
        time.sleep(20)
    else:
        print("list_metrics_result len: ", len(list_metrics_result))
        disk_used_percent_metric = list_metrics_result[0]
        print("disk_used_percent_metric: ", disk_used_percent_metric)
        alarm = cloudwatchClient.put_metric_alarm(AlarmName='MyChordFileSystemASGDiskUsedAlarm',
                                                  AlarmActions=[
                                                      policy['PolicyARN']],
                                                  Metrics=metrics,
                                                  EvaluationPeriods=2,
                                                  Threshold=24,
                                                  ComparisonOperator='GreaterThanThreshold')
        print("alarm: ", alarm)
        break


print("finish")
