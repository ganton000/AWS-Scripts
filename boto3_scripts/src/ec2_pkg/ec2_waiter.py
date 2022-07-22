##Waiters await operations that run asynchronously
import boto3
import time

profileName = "default"

def start_ec2_with_resource_waiter(profileName, instance_id):
	aws_mng_con = boto3.session.Session(profile_name=profileName)

	ec2_con_res = aws_mng_con.resource(service_name='ec2', region_name='us-east-1')

	my_instance = ec2_con_res.Instance(instance_id)
	print("Starting instance.....")
	my_instance.start()
	print("The instance is currently ", my_instance.state['Name'])

	'''
	#Self-made Waiter logic
	while True:
		print("The current status of EC2 instance is: ", my_instance.state['Name'])
		if my_instance.state['Name'] == "running":
			break
		print("Waiting to get running status....")
		time.sleep(5)
	'''

	#print(dir(my_instance))

	"""
	creates Resource waiter which awaits until ec2 instance is running (or starts)
	The waiter waits 40times, in 5 second breaks
	After 200 seconds is passed, boto3 throws an exception
	"""
	my_instance.wait_until_running()
	print("Instance is now up and running")

def start_ec2_with_client_waiter(profileName, instance_id):

	aws_mng_con = boto3.session.Session(profile_name=profileName)
	#setup client
	ec2_con_client = aws_mng_con.client(service_name='ec2', region_name='us-east-1')

	print("Starting EC2 instance...")
	ec2_con_client.start_instances(InstanceIds=[instance_id])

	'''
	creates waiter and waits
	client waiter has 40 checks every 15 seconds
	so client waiters are preferred
	'''
	waiter = ec2_con_client.get_waiter("instance_running")
	waiter.wait(InstanceIds=[instance_id])

	print("Now your EC2 instance is up and running!")

##Note you can attach waiter from client and start ec2 instance using resource if you wanted longer waiter (600 seconds ~ 10 mins; instead of 200 seconds)