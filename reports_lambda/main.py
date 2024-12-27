import boto3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import io
import os
import re

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    table_name = os.environ['DYNAMODB_TABLE']
    bucket_name = os.environ['S3_BUCKET']
    data = fetch_data(table_name)
    pdf_buffer = generate_plots(data)
    upload_to_s3(pdf_buffer, bucket_name)

def fetch_data(table_name):
    table = dynamodb.Table(table_name)
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    
    return data

def generate_plots(data):
    stations = {}
    for item in data:
        station = item['station']
        timestamp = datetime.datetime.strptime(item['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z")
        pm10 = float(re.sub('[^\d.]+', '', item['pm10']))
        
        if station not in stations:
            stations[station] = []
        stations[station].append((timestamp, pm10))
    
    pdf_buffer = io.BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        for station, values in stations.items():
            values.sort()  
            times, pm10_values = zip(*values)
            plt.figure(figsize=(10, 6))
            plt.plot(times, pm10_values, marker='o')
            plt.title(f"PM10 Levels over Time for {station}")
            plt.xlabel("Time")
            plt.ylabel("PM10 (mg/m³)")
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            pdf.savefig()
            plt.close()
    pdf_buffer.seek(0)  
    return pdf_buffer

def upload_to_s3(pdf_buffer, bucket_name):
    s3.upload_fileobj(pdf_buffer, bucket_name, 'air_quality_report.pdf')

