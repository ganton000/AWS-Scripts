#Collections exist under resource console
import boto3

profileName = 'default'

aws_manage_console = boto3.session.Session(profile_name=profileName)
ec2_con_res = aws_manage_console.resource(service_name='ec2', region_name='us-east-1')

stopped_filter = [{
	"Name": "instance-state-name",
	"Values": ["stopped"]
}]

run_stopped_filter = {
	"Name": "instance-state-name",
	"Values": ["running", "stopped"]
}

t2_micro_filter = {
	"Name": "instance-type",
	"Values": ["t2.micro"]
}


def get_and_filter_instance_collection_object(Filters=[]):
	for each in ec2_con_res.instances.filter(Filters=Filters):
		print(each)

#get_and_filter_instance_collection_object(stopped_filter) #stopped instances

##Filters for running OR stopped instances, with instance type t2.micro
get_and_filter_instance_collection_object([run_stopped_filter, t2_micro_filter])
