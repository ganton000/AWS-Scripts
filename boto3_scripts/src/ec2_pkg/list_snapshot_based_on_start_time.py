from tracemalloc import start
from list_all_snapshots import *
import datetime


if __name__ == "__main__":

	profileName = "default"
	aws_mag_con = boto3.session.Session(profile_name=profileName)
	ec2_con_res = aws_mag_con.resource(service_name='ec2', region_name='us-east-1')

	today = datetime.datetime.now()
	start_time = datetime.datetime(today.year, today.month, today.day,16,00,00) #4:00:00 pm

	print(start_time)

	snapshots = get_all_snapshots(profileName)
	if snapshots:
		for snapshot in snapshots:
			if snap_start_time == start_time:
				snap_id = snapshot.id
				snap_start_time = snapshot.start_time.strftime("%Y-%m-%d %H:%M:%S")
				print(f"Snapshot with id {snap_id} was created on {snap_start_time}")
	else:
		print("No snapshots available!")
