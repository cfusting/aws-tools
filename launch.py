import boto3
import argparse
from pprint import pformat
import time
import logging

parser = argparse.ArgumentParser(description='Connect to EC2 Instance and attach drive.')
parser.add_argument('-v', '--verbose', help='Verbose.', action='store_true')
parser.add_argument('-t', '--type', help='Node type')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.INFO)

ec2 = boto3.client('ec2')
image_id = 'ami-c044aeba'
response = ec2.request_spot_instances(
    InstanceCount=1,
    DryRun=False,
    LaunchSpecification={
        'ImageId': image_id,
        'InstanceType': args.type,
        'KeyName': 'cfusting-key-pair-n-virginia',
        'Placement': {
            'AvailabilityZone': 'us-east-1e',
        },
        'SecurityGroupIds': [
            'sg-05711676',
        ],
        'SubnetId': 'subnet-c035a7eb',
    },
    SpotPrice='0.45',
    Type='one-time',
)
logging.info(pformat(response))
spot_instance_request_id = response['SpotInstanceRequests'][0]['SpotInstanceRequestId']
logging.info('Waiting for request to be fulfilled.')
public_ip = None
instance_id = None
looking = True
while looking:
    time.sleep(0)
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'spot-instance-request-id',
                'Values': [
                    str(spot_instance_request_id),
                ]
            },
        ],
        DryRun=False,
        MaxResults=10
    )
    for res in response['Reservations']:
        for ins in res['Instances']:
            if ins['State']['Code'] == 16:
                looking = False
                logging.info(pformat(response))
                logging.info("Spot instance fulfilled!")
                instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']
                logging.info("Instance ID: " + instance_id)
                logging.info("Public DNS: " + response['Reservations'][0]['Instances'][0]['PublicDnsName'])
                public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
                logging.info("Public IP: " + public_ip)
                print(public_ip)
resource = boto3.resource('ec2')
volume_id = 'vol-09a37de1b3d2a45d1'
device = '/dev/sdy'
logging.info('Attaching Volume: ' + volume_id + ' on instance: ' + instance_id + ' to device: ' + device)
resource.Instance(instance_id).attach_volume(VolumeId=volume_id, Device=device)
