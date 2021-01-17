print("Starting blue/green deployment")
import boto3
import time

start = time.time()

ec2 = boto3.client('ec2')
elb = boto3.client('elbv2')

instance_name = "tdev_blue"
to_delete = ""
user_data = open("user_data.sh", "r").read()

# determine color
response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                'tdev_blue',
                'tdev_green'
            ]
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]
)
if len(response['Reservations']) == 0:
    print('No Existing deployment defaulting to blue')
elif len(response['Reservations']) == 1:
    if response['Reservations'][0]['Instances'][0]['Tags'][0]['Value'] == 'tdev_blue':
        instance_name = 'tdev_green'
        to_delete = 'tdev_blue'
        print('Found blue, building green')
    else:
        instance_name = 'tdev_blue'
        to_delete = 'tdev_green'
        print('Found green, building blue')
else:
    print('More than expected deployemnts, please delete it manually')
    exit()


# create instance
print(f'Creating {instance_name} instance')
response = ec2.run_instances(
    ImageId='ami-0885b1f6bd170450c',
    InstanceType='t2.nano',
    SecurityGroupIds=[
        'sg-03d06481bfec4701f',
    ],
    MaxCount=1,
    MinCount=1,
    SubnetId='subnet-099e8ac0172011cea',
    UserData= user_data,
    KeyName='m1_mac',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': instance_name
                }
            ]
        }
    ]
)
instance_id = response['Instances'][0]['InstanceId']
print(f'Instance created {instance_id}')

# Wait for instance state to become running
for i in range(1,11):
    print(f'Waiting for 10s for instance state to become running ({i}/10)')
    time.sleep(10)
    response = ec2.describe_instance_status(
        InstanceIds=[
            instance_id,
        ],
    )
    if response['InstanceStatuses'] != [] and \
        response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running':
        print('Instance is running!')
        break

    if i==10:
        print('FAILURE, Timeout')
        exit()

# register target 
print('Register target')
elb.register_targets(
    TargetGroupArn='arn:aws:elasticloadbalancing:us-east-1:642333780766:targetgroup/tg-def/422948bcc92b9333',
    Targets=[
        {
            'Id': instance_id,
            'Port': 3000,
        },
    ]
)

# check for target health
for j in range(1,31):
    print(f'Waiting for 10s for target to reach healthy status ({j}/30)')
    time.sleep(10)
    response = elb.describe_target_health(
        TargetGroupArn='arn:aws:elasticloadbalancing:us-east-1:642333780766:targetgroup/tg-def/422948bcc92b9333',
        Targets=[
            {
                'Id': instance_id,
                'Port': 3000,
            },
        ]
    )
    if response['TargetHealthDescriptions'][0]['TargetHealth']['State'] == 'healthy':
        print('Target is healthy')
        break

    if j==30:
        print('FAILURE, Timeout')
        exit()

# destroy old deployment
if to_delete != "":
    print(f'Destroying {to_delete}')
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    to_delete
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    instance_id_to_delete = response['Reservations'][0]['Instances'][0]['InstanceId']

    ec2.terminate_instances(
        InstanceIds=[
            instance_id_to_delete,
        ]
    )
print(f'SUCCESS, Deployment completed in {int(time.time()-start)} seconds')

