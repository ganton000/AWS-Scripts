import boto3
import csv

profileName = 'default'

aws_mag_con = boto3.session.Session(profile_name=profileName)
ec2_con_res = aws_mag_con.resource(service_name='ec2', region_name='us-east-1')

csv_obj = open("inventory_info.csv", "w", newline='')
csv_w = csv.writer(csv_obj)
csv_w.writerow(["SERIAL_NO", "Instance_Id", "Instance_Type", "Architecture", "LaunchTime", "Private_Ip"])


def export_data_into_csv_file(csv_writer):
	'''
	The file is overwritten rather than appended
	'''
	print("Writing data into CSV")
	count = 1
	for instance in ec2_con_res.instances.all():
		print(count, instance, instance.instance_id, instance.instance_type, instance.architecture, instance.launch_time.strftime("%Y-%m-%d"), instance.private_ip_address)
		csv_writer.writerow([count, instance, instance.instance_id, instance.instance_type, instance.architecture, instance.launch_time.strftime("%Y-%m-%d"), instance.private_ip_address])
		count += 1
	print("Completed writing data into CSV")

export_data_into_csv_file(csv_w)