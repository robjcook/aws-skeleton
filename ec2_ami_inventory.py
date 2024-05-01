import boto3
import xlsxwriter

def get_all_amis():
    ec2 = boto3.client('ec2')
    amis = ec2.describe_images(Owners=['self'])['Images']
    return amis

def write_to_excel(amis):
    workbook = xlsxwriter.Workbook('aws_amis_inventory.xlsx')
    worksheet = workbook.add_worksheet()

    # Write headers
    headers = ['AMI ID', 'Name', 'Description', 'Creation Date']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write data
    row = 1
    for ami in amis:
        worksheet.write(row, 0, ami['ImageId'])
        worksheet.write(row, 1, ami.get('Name', 'N/A'))
        worksheet.write(row, 2, ami.get('Description', 'N/A'))
        worksheet.write(row, 3, str(ami['CreationDate']))
        row += 1

    workbook.close()

def main():
    amis = get_all_amis()
    write_to_excel(amis)

if __name__ == "__main__":
    main()
