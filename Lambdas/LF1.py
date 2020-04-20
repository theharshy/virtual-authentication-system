import json
import boto3
import datetime
import logging
import base64
from ast import literal_eval
from boto3.dynamodb.conditions import Key
import random
import time
from os import listdir
from botocore.exceptions import ClientError

import sys
sys.path.insert(1, '/opt')
import cv2

owner = 'YOUR-EMAIL-ADDRESS' 
def send_sns_message(phone_number, txt_message):
    sns_client = boto3.client("sns")
   
    try:
        text_number = "+{}".format(phone_number)
        msg = sns_client.publish(
                    PhoneNumber=text_number,
                    Message=txt_message
                )
    except ClientError as e:
        print(e)
        return None
    return msg
def send_ses_message(email, message):
    ses_client = boto3.client("ses")
   
    try:
        ses_client.send_email(
            Destination={
        'Source': owner,
        'ToAddresses': [
            email
        ]},
        Message={
        'Subject': {
            'Data': 'abcd',
            'Charset': 'utf8'
        },
        'Body': {
            'Text': {
                'Data': message,
                'Charset': 'utf8'
            }
        }
    })
    except ClientError as e:
        print(e)
        return None
    return msg
my_stream_name = 'ks1'
def lambda_handler(eventer, context):
    client = boto3.client('rekognition')
    response = client.stop_stream_processor(
    Name='balagurustream'
    )
    response = client.start_stream_processor(
    Name='balagurustream'
    )
    send_sns_message(owner,"test")
#     print(listdir("/opt"))
#     print('version number', cv2.__version__)
#     kvs_client = boto3.client('kinesisvideo')
#     kvs_data_pt = kvs_client.get_data_endpoint(
#         # StreamName='BalaGuruSwami',
#         StreamARN='arn:aws:kinesisvideo:us-east-1:482044356813:stream/BalaGuruSwami/1572652212725',
#         APIName='GET_MEDIA'
#     )
    
#     print(kvs_data_pt)
    
#     end_pt = kvs_data_pt['DataEndpoint']
#     kvs_video_client = boto3.client('kinesis-video-media', endpoint_url=end_pt, region_name='us-east-1')
#     kvs_stream = kvs_video_client.get_media(
#         StreamARN='arn:aws:kinesisvideo:us-east-1:482044356813:stream/BalaGuruSwami/1572652212725',
#         StartSelector={'StartSelectorType': 'EARLIEST'}
#     )
#     print(kvs_stream)
    
#     # print(streamBody.read())
    
#     s_time = time.time()
#     with open('/tmp/stream.mkv', 'wb') as f:
#         streamBody = kvs_stream['Payload'].read(1024*16384)
#         f.write(streamBody)
#         # use openCV to get a frame
#         print('here')
#         cap = cv2.VideoCapture('/tmp/stream.mkv')
#         # length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         # print(length)
#         # our logic - get a frame around median of the frames
#         # if you have some other logic to determine if the person is present in the frame like using bounding box etc, go ahead and use it
#         # cap.set(2, length/2)
#         ret, frame = cap.read()
        
#         cv2.imwrite('/tmp/frame.jpg', frame)
#         s3_client = boto3.client('s3')
#         s3_client.upload_file(
#             '/tmp/frame.jpg',
#             'balagurubucket',
#             'frame.jpg'
#         )
# #         s3_client = boto3.resource('s3')
# #         bucket = s3_client.Bucket('balagurubucket')
# #         dest_object_name = 'hello.mp4'
    
# #         bucket.upload_file('/tmp/hello.mkv', dest_object_name)
#         cap.release()
#         print('Image uploaded')
    
    kinesis_client = boto3.client('kinesis', region_name='us-east-1')
    response = kinesis_client.describe_stream(StreamName=my_stream_name)
    my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']

    shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name,
                                                      ShardId=my_shard_id,
                                                      ShardIteratorType='LATEST')

    my_shard_iterator = shard_iterator['ShardIterator']
    event = kinesis_client.get_records(ShardIterator=my_shard_iterator,
                                              Limit=2)

    while 'NextShardIterator' in event and len(event['Records'])==0:
        event = kinesis_client.get_records(ShardIterator=event['NextShardIterator'],
                                                  Limit=2)

    print(event)

    # # wait for 5 seconds
    # time.sleep(5)
    face ="123"
    
    count = 0
    for record in event['Records']:
        if count==20:
            break
        print(record)
        # load = base64.b64decode(record['kinesis']['data'])
        # load = load.decode("utf-8")
        
        # load = json.loads(load)
        # print(load)
        load = json.loads(record['Data'])
        print("load : ", load)
        if load['FaceSearchResponse'] and load['FaceSearchResponse'][0]['MatchedFaces']:
            face = load['FaceSearchResponse'][0]['MatchedFaces'][0]['Face']['FaceId']
            break
        count = count+1
    print(face)
    
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
    table = dynamodb.Table('visitors')
    response1 = table.query(
        KeyConditionExpression=Key('faceID').eq(face))
    print("out here")
    if(len(response1['Items'])!=0):
        print("in here")
        otp = random.randrange(1000, 10000)
        print("otp" + str(otp))
        return_val = send_sns_message(response1['Items'][0]['phone'], str(otp))
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://dynamodb.us-east-1.amazonaws.com")
        table = dynamodb.Table('passcodes')
        ep = datetime.datetime(1970,1,1,0,0,0)
        x = int((datetime.datetime.utcnow()- ep).total_seconds() +300)
        table.put_item(
        Item={
          "userID" : face,
          "Code" : str(otp),
          "epoch_datetime" : x
          })
    else:
        url = "PHOTO-URL"
        print("sending sns")
        send_ses_message(owner,"/Frontend/index.html?imageurl=" + url)
    
    response = client.stop_stream_processor(
    Name='balagurustream'
    )
    
    print("reaching here")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }