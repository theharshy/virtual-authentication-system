import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
import random
from botocore.exceptions import ClientError

def send_sns_message(phone_number, txt_message):
    sns_client = boto3.client("sns")
   
    try:
        text_number = phone_number
        msg = sns_client.publish(
                    PhoneNumber=str(text_number),
                    Message=txt_message
                )
    except ClientError as e:
        print(e)
        return None
    return msg

def lambda_handler(event, context):
    # TODO implement
    bucket = "PHOTOS-BUCKET-URL"
    if event['number'] is not None:
        currenTimeStamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # parts =  event['imageurl'].split('m/')
        # bucket = parts[0] + 'm/'
        # objectKey = parts[1]
        objectKey = event['name']+".jpg"
        print(event)
        if(len(event['faceid'])==0 or event['faceid']=="undefined"): 
            client=boto3.client('rekognition')
            response=client.index_faces(CollectionId= 'mycollection',
            Image={'S3Object':{'Bucket': 'NAME','Name': objectKey}},
            ExternalImageId=objectKey,
            DetectionAttributes=['ALL'])
            
            event['faceid'] = response['FaceRecords'][0]['Face']['FaceId']

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
        table = dynamodb.Table('visitors')
        response = table.query(
        KeyConditionExpression=Key("faceID").eq(event['faceid']))
        if len(response['Items']) == 0:
            table.put_item(
            Item={
              "faceID" : event['faceid'],
              "phone" : event['number'],
              "name" : event['name'],
              "photos" : [{ "objectKey" : objectKey , "bucket" :bucket , "createdTimestamp" :currenTimeStamp}]
              })
        else:
            result = table.update_item(
            Key={
                'faceID': event['faceid']
            },
            UpdateExpression="SET photos = list_append(photos, :i)",
            ExpressionAttributeValues={
                ':i': [{ "objectKey" : objectKey  , "bucket" :bucket , "createdTimestamp" :currenTimeStamp}],
            },
            ReturnValues="UPDATED_NEW"
            )
            print(result)
        
        otpTable = dynamodb.Table('passcodes')
        otp = random.randrange(1000, 10000)
        ep = datetime(1970,1,1,0,0,0)
        x = int((datetime.utcnow()- ep).total_seconds() +300)
        otpTable.put_item(
        Item={
          "userID" : event['faceid'],
          "Code" : str(otp),
          "epoch_datetime" : x
          })
        print("otp" + str(otp))
        retVal = send_sns_message(event['number'], "OTP = " + str(otp))
          
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
