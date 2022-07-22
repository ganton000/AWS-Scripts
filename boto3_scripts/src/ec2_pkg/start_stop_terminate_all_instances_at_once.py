import boto3
import asyncio

profileName = 'default'

aws_manage_console = boto3.session.Session(profile_name=profileName)
ec2_con_res = aws_manage_console.resource(service_name='ec2', region_name='us-east-1')

def get_ids_of_stopped_instances():
	filter = [{
	"Name": "instance-state-name",
	"Values": ["stopped"] }]

	res_list = []
	for each_instance in ec2_con_res.instances.filter(Filters=filter):
		res_list.append(each_instance.id)

	return res_list

def get_ids_of_started_instances():
	filter = [{
	"Name": "instance-state-name",
	"Values": ["running"] }]

	res_list = []
	for each_instance in ec2_con_res.instances.filter(Filters=filter):
		res_list.append(each_instance.id)

	return res_list

def start_all_stopped_instances():
	print("Starting all instances.... ")
	list_of_instances_to_start = get_ids_of_stopped_instances()
	ec2_con_res.instances.start()
	waiter = ec2_con_res.meta.client.get_waiter('instance_running')
	waiter.wait(InstanceIds=list_of_instances_to_start)
	print("All instances are up and running")

#start_all_stopped_instances()

def stop_all_running_instances():
	print("Stopping all running instances.... ")
	list_of_instances_to_stop = get_ids_of_started_instances()
	ec2_con_res.instances.stop()
	waiter = ec2_con_res.meta.client.get_waiter('instance_stopped')
	waiter.wait(InstanceIds=list_of_instances_to_stop)
	print("All running instances have been stopped")

#stop_all_running_instances()

tag = ["env", "non-prod"]

def filter_instances_by_tag(tag):
	filter = [{
	"Name": f'tag:{tag[0]}',
	"Values": [ tag[1] ] }]

	res_list = []
	for each_instance in ec2_con_res.instances.filter(Filters=filter):
		res_list.append(each_instance.id)

	return res_list

async def start_all_instances_by_tag(tag):
	'''
	Can only use client to start instances by specific ids, otherwise
	resource object starts all instances.
	To filter instances without using resource object (resource.instances.filter(Filters=filter) can use
	client.describe_instances(Filters=filter) with same filter format.
	'''
	ec2_con_client = aws_manage_console.client(service_name='ec2', region_name='us-east-1')
	print(f"Starting all instances with tag: {tag[0]}: {tag[1]}")
	list_of_instances_to_start = filter_instances_by_tag(tag)
	await asyncio.sleep(1)
	ec2_con_client.start_instances(InstanceIds=list_of_instances_to_start)
	waiter = ec2_con_client.get_waiter('instance_running')
	waiter.wait(InstanceIds=list_of_instances_to_start)
	print("All instances are up and running")

#asyncio.run(start_all_instances_by_tag(tag))

def start_all_instances_with_resource_by_tag(tag):
	ec2_con_client = aws_manage_console.client(service_name='ec2', region_name='us-east-1')

	print(f"Starting all instances with tag: {tag[0]}: {tag[1]}")

	filter = [{
		"Name": f'tag:{tag[0]}',
		"Values": [ tag[1] ]
		}]

	filtered_list = []
	for each_item in ec2_con_client.describe_instances(Filters=filter)['Reservations']:
		for each_instance in each_item['Instances']:
			filtered_list.append(each_instance['InstanceId'])

	print(f"The Instance Ids corresponding to the tags are: {filtered_list}")

	ec2_con_client.start_instances(InstanceIds=filtered_list)
	waiter = ec2_con_client.get_waiter('instance_running')
	waiter.wait(InstanceIds=filtered_list)
	print("All instances are up and running")

#start_all_instances_with_resource_by_tag(tag)

def stop_all_instances_by_tag(tag):
	ec2_con_client = aws_manage_console.client(service_name='ec2', region_name='us-east-1')
	print(f"Stopping all instances with tag: {tag[0]}: {tag[1]}")
	list_of_instances_to_start = filter_instances_by_tag(tag)
	ec2_con_client.stop_instances(InstanceIds=list_of_instances_to_start)
	waiter = ec2_con_client.get_waiter('instance_stopped')
	waiter.wait(InstanceIds=list_of_instances_to_start)
	print(f"All instances with tag value: {tag[1]} have been stopped")

#stop_all_instances_by_tag(tag)


def stop_all_instances_with_resource_by_tag(tag):
	ec2_con_client = aws_manage_console.client(service_name='ec2', region_name='us-east-1')

	print(f"Stopping all instances with tag: {tag[0]}: {tag[1]}")

	filter = [{
		"Name": f'tag:{tag[0]}',
		"Values": [ tag[1] ]
		}]

	filtered_list = []
	for each_item in ec2_con_client.describe_instances(Filters=filter)['Reservations']:
		for each_instance in each_item['Instances']:
			filtered_list.append(each_instance['InstanceId'])

	print(f"The Instance Ids corresponding to the tags are: {filtered_list}")

	ec2_con_client.stop_instances(InstanceIds=filtered_list)
	waiter = ec2_con_client.get_waiter('instance_stopped')
	waiter.wait(InstanceIds=filtered_list)
	print("The instances {filtered_list} are now stopped")

#stop_all_instances_with_resource_by_tag(tag)