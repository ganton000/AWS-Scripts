import boto3

profileName="default"

aws_mag_con = boto3.session.Session(profile_name=profileName)
ec2_con_res = aws_mag_con.resource(service_name="ec2", region_name="us-east-1")

def get_all_ebs_volumes():
	for volume in ec2_con_res.volumes.all():
		print(f"The volume id is: {volume.id}, and it's state is: {volume.state}")

#get_all_ebs_volumes()

filter_ebs_in_use = {
	"Name": "status",
	"Values": ["in-use"]
}

def get_ebs_volumes_by_filter_and_display_tag(filters=[]):
	for volume in ec2_con_res.volumes.filter(Filters=filters):
		print(f"This in-use ebs volume has id: {volume.id}, and has tags: {volume.tags}")


#get_ebs_volumes_by_filter_and_display_tag([filter_ebs_in_use])

def delete_untagged_and_in_use_ebs_volumes(filters=[]):
	for volume in ec2_con_res.volumes.filter(Filters=filters):

		if not volume.tags:
			print(f"This in-use and untagged ebs volume has id: {volume.id}")
			print("Now deleting this volume...")
			volume.detach_from_instance(InstanceId=volume.id)
			waiter = ec2_con_res.meta.client.get_waiter(Filters=[{"Name": "attachment.status", "Values": ["detaching"] }])
			waiter.wait(InstanceIds=[volume.id])
			volume.delete()

	print("Deleted all unused and untagged volumes.")

#delete_untagged_and_in_use_ebs_volumes(filters=[filter_ebs_in_use])

ec2_con_client = aws_mag_con.client(service_name="ec2", region_name="us-east-1")

def get_volumes_and_delete_with_client():
	'''
	If Volume is in-use then must detach and make available prior to deletion.
	'''
	for vol_obj in ec2_con_client.describe_volumes()['Volumes']:

		if vol_obj.get('Tags', 'No Tags') == 'No Tags' and vol_obj['State'] == 'available':
			print(f"VolumeId with Available State and No Tags is: {vol_obj['VolumeId']}")
			print("Deleting", vol_obj['VolumeId'])
			ec2_con_client.delete_volume(VolumeId=vol_obj['VolumeId'])
			print('Deleted all unused and untagged volumes')
		else:
			print(f"VolumeId: {vol_obj['VolumeId']},\nVolume State: {vol_obj['State']},\nVolume Tags: {vol_obj.get('Tags', 'No Tags')}")

get_volumes_and_delete_with_client()