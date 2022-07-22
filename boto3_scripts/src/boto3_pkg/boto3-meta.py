#meta object is used to enter into client object from resource
import boto3

profileName = 'default'


def list_all_regions_for_ec2(profileName):
	aws_manage_con = boto3.session.Session(profile_name=profileName)
	ec2_con_res = aws_manage_con.resource(service_name='ec2', region_name='us-east-1')
	return [ print(item['RegionName']) for item in ec2_con_res.meta.client.describe_regions()['Regions'] ]

list_all_regions_for_ec2(profileName)