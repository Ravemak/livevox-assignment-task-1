import boto3
import os
import sys
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_asg_client():
    return boto3.client('autoscaling', region_name=os.environ.get('AWS_REGION', 'ap-south-1'))

def get_ec2_client():
    return boto3.client('ec2', region_name=os.environ.get('AWS_REGION', 'ap-south-1'))

def verify_asg(asg_name):
    asg_client = get_asg_client()
    ec2_client = get_ec2_client()

    try:
        response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
        if not response['AutoScalingGroups']:
            logger.error(f"No Auto Scaling Group found with the name {asg_name}")
            return
        asg = response['AutoScalingGroups'][0]
        
        # Test Case A
        instances = asg['Instances']
        if asg['DesiredCapacity'] != len(instances):
            print("Test Case A - Fail: Desired capacity does not match the number of instances")
        else:
            print("Test Case A - Pass: Desired capacity matches the number of instances")
        
        availability_zones = set(instance['AvailabilityZone'] for instance in instances)
        if len(instances) > 1 and len(availability_zones) == 1:
            print("Test Case A - Fail: Instances are not distributed across multiple availability zones")
        else:
            print("Test Case A - Pass: Instances are distributed across multiple availability zones")
        
        security_group = instances[0]['SecurityGroups'][0]['GroupId']
        image_id = instances[0]['ImageId']
        vpc_id = instances[0]['VpcId']
        
        security_group_match = all(instance['SecurityGroups'][0]['GroupId'] == security_group for instance in instances)
        image_id_match = all(instance['ImageId'] == image_id for instance in instances)
        vpc_id_match = all(instance['VpcId'] == vpc_id for instance in instances)
        
        if security_group_match and image_id_match and vpc_id_match:
            print("Test Case A - Pass: Security Group, Image ID, and VPC ID match for all instances")
        else:
            print("Test Case A - Fail: Security Group, Image ID, or VPC ID mismatch")
        
        longest_uptime_instance = max(instances, key=lambda x: x['LaunchTime'])
        print("Longest uptime instance:", longest_uptime_instance)
        
        # Test Case B
        scheduled_actions = asg.get('ScheduledActions', [])
        if scheduled_actions:
            next_scheduled_action = min(scheduled_actions, key=lambda x: x['StartTime'])
            current_time = datetime.utcnow()
            time_remaining = next_scheduled_action['StartTime'] - current_time
            print("Time remaining for next scheduled action:", time_remaining)
        else:
            print("No scheduled actions")
        
        instance_stats = ec2_client.describe_instance_status(IncludeAllInstances=True)
        current_day = datetime.utcnow().date()
        launched_instances = 0
        terminated_instances = 0
        
        for instance in instance_stats['InstanceStatuses']:
            launch_time = instance['InstanceState']['LaunchTime']
            launch_date = launch_time.date()
            
            if launch_date == current_day:
                launched_instances += 1
            
            if instance['InstanceState']['Name'] == 'terminated' and launch_date == current_day:
                terminated_instances += 1
        
        print("Launched instances today:", launched_instances)
        print("Terminated instances today:", terminated_instances)
    
    except Exception as e:
        logger.exception("An error occurred")

def main():
    if len(sys.argv) > 1:
        asg_name = sys.argv[1]
        verify_asg(asg_name)
    else:
        logger.error("Please pass the Auto Scaling Group name as an argument.")
        logger.info("Usage: ./sample-test.py asgname")

if __name__ == "__main__":
    main()    
