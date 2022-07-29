import boto3


def get_owner_id():
	sts_client = session.client(service_name="sts", region_name=source_region)
	account_id = sts_client.get_caller_identity().get('Account')

	return account_id

filter_backup = {
	'Name': 'tag:backup',
	'Values': ['yes']
}

def get_ebs_snapshots_by_filter(ec2_client, ownerId, filter={}):

	snapIds_to_backup=[]
	for each_snap in ec2_client.describe_snapshots(OwnerIds=[ownerId],Filters=[filter]).get('Snapshots'):
		snapIds_to_backup.append(each_snap.get('SnapshotId'))

	return snapIds_to_backup


def make_copy_of_ebs(dest_region, source_region, snapshots_to_copy: list):
	ec2_dest_client = session.client(service_name="ec2", region_name=dest_region)

	for each_snap_id in snapshots_to_copy:
		print(f"Taking backup for id of {each_snap_id} for region {dest_region}")

		ec2_dest_client.copy_snapshot(
			Description=f"Copy of snapshot: {each_snap_id} from {dest_region} for disaster recovery",
			SourceRegion= source_region,
			SourceSnapshotId= each_snap_id
		)
	print(f"EBS Snapshot copy to destination region {dest_region} is completed")

def delete_and_create_new_tags(client, snapshotIds):

	print("Deleting tags for the snapshots for which backup is completed")

	tags_to_delete = {
		'Key': 'backup',
		'Value': 'yes'
	}

	tags_to_create = {
		'Key': 'backup',
		'Value': 'completed'
	}
	for each_snap_id in snapshotIds:
		print("Deleting old tag for snapshot id: ", each_snap_id)
		client.delete_tags(
			Resources=[each_snap_id],
			Tags=[tags_to_delete]
		)

		print("Creating new tag for snapshot id: ", each_snap_id)
		client.create_tags(
			Resources=[each_snap_id],
			Tags=[tags_to_create]
		)





if __name__ == "__main__":

	source_region= 'us-east-1'
	dest_region = 'us-east-2'
	profileName= 'default'

	session= boto3.session.Session(profile_name=profileName)
	ec2_source_client= session.client(service_name='ec2', region_name=source_region)

	ownerId= get_owner_id()

	snapIds_to_backup= get_ebs_snapshots_by_filter(ec2_source_client, ownerId, filter_backup)

	make_copy_of_ebs(dest_region, source_region, snapIds_to_backup)

	delete_and_create_new_tags(client=ec2_source_client, snapshotIds=snapIds_to_backup)
