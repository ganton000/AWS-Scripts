#!/usr/bin/python3
import boto3

def list_ec2_instances_with_iam_role(profileName):
	ec2_con = boto3.resource(service_name="ec2", region_name="us-east-1")

	return [ print(each_instance.id, each_instance.state) for each_instance in ec2_con.instances.all()]

list_ec2_instances_with_iam_role("default")
