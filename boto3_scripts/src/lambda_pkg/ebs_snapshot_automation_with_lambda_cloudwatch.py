'''
Can run this script as cronjob through linux server
will do this with AWS Lambda and CloudWatch event trigger instead

IAM Role should have EC2 Permissions
(ensure Timeout for Lambda is sufficient)
'''

import boto3

ec2_client = boto3.client("ec2", "us-east-1")

filter_prod_backup = {
		'Name': 'tag:Prod',
		'Values': ['backup', 'Backup']
	}

def list_all_ebs_volumes_with_filter(filter):

	vol_iter = ec2_client.describe_volumes(Filters=[filter])['Volumes']

	if len(vol_iter) == 0: return None
	else:
		list_of_vol_ids= []
		for each_vol in vol_iter:
			list_of_vol_ids.append(each_vol['VolumeId'])

	return list_of_vol_ids


#list_all_ebs_volumes_with_filter(filter_prod_backup)

def paginate_over_ebs_volumes_with_filter(filter, client=ec2_client):
	paginator = ec2_client.get_paginator("describe_volumes")
	for each_page in paginator.paginate(Filters=[filter]):

		if len(each_page['Volumes']) == 0: return None
		else:
			list_of_vol_ids= []

			for each_vol in each_page['Volumes']:
				list_of_vol_ids.append(each_vol['VolumeId'])

	return list_of_vol_ids

list_of_volids = paginate_over_ebs_volumes_with_filter(filter_prod_backup)

def generate_snapshot_of_volid(volids: list, client=ec2_client):
	snapids = []
	if not list_of_volids:
		print("No Volume Ids available to take snapshots for this region")
		return None
	for each_volid in list_of_volids:
		print(f"Taking snap of {each_volid}")
		res = ec2_client.create_snapshot(
			Description="Taking snap with Lambda and CW",
			VolumeId=each_volid,
			TagSpecifications=[{
				'ResourceType': 'snapshot',
				'Tags': [{
					'Key': 'Delete-on',
					'Value': '90-days'
				}]
			}]
		)
		snapids.append(res.get('SnapshotId'))

	print(f'The snap ids are: {snapids}')

	waiter = ec2_client.get_waiter('snapshot_completed')
	waiter.wait(SnapshotIds=[snapids])

	print(f"Successfully completed snapshots for the volumes with ids {volids}")

	return None


generate_snapshot_of_volid(list_of_volids)
