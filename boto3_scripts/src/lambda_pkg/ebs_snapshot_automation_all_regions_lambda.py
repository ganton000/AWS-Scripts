import boto3
from .ebs_snapshot_automation_with_lambda_cloudwatch import paginate_over_ebs_volumes_with_filter, generate_snapshot_of_volid

profileName = "default"

session = boto3.session.Session(profile_name=profileName)
ec2_client = session.client(service_name="ec2", region_name="us-east-1")

def get_all_regions_for_ebs_volumes() -> list:
	all_regions = []
	for each_region in ec2_client.describe_regions()['Regions']:
		all_regions.append(each_region.get('RegionName'))

	return all_regions

def create_snapshot_for_each_region():
	all_regions = get_all_regions_for_ebs_volumes()

	for each_region in all_regions:
		ec2_client_region = session.client(service_name="ec2", region_name=each_region)
		print(f'Working on region: {each_region}')

		list_of_volids = paginate_over_ebs_volumes_with_filter(filter=[], client=ec2_client_region)

		#If no volids, then no snapshots necessary
		if bool(list_of_volids) == False:
			continue

		generate_snapshot_of_volid(volids=list_of_volids, client=ec2_client_region)