import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
import random
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # TODO implement
    otp = event['otp']
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    table = dynamodb.Table('passcodes')
    print("otp" + str(otp))
    response = table.query(
        KeyConditionExpression=Key('Code').eq(str(otp))) 
    
    if(len(response['Items'])!=0):
        print("coming here")
        return {
            'statusCode': 200,
            'body': True
        }
    else:
        print("access denied")
        return {
            'statusCode': 404,
            'body': False
        }
    
        