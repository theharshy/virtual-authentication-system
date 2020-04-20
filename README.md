# Smart Door Authentication System

In this project, me and my team implemented a smart door authentication system which made use of Amazon AWS Cloud based services including but not limited to Kinesis Video Streams and Amazon Rekognition. We built a distributed system for authenticating people with the access to a virtual door by extracting and recognizing their faces from video captured at the user end.

The pipeline is as follows:
1. The video containing the user’s face is captured using the Kinesis Video Stream. The video is passed through the Amazon Recognition service and the detected face’s ID is sent to a lambda function (LF1).
2. The LF1 lambda function is connected two DynamoDB databases, D1 (which stores the face ID) and D2 (which stores OTP). It first checks whether the detected face ID is present in the D1. Two actions are possible:
    1. If the face is present in D1, an OTP is generated and stored with a life of 5 minutes in D2. The OTP is sent to the user through Amazon’s SNS service.
    2. If the face is not in the database, a notification is sent to the owner.
3. For the unknown face, if the owner grants permission to the new face, a lambda function LF2 is triggered. The face ID gets stored in the database D1. Additionally, an OTP is generated and stored with a life of 5 minutes in D2. The OTP is sent to the user.
4. Once the user gets an OTP, he enters it into the system and another lambda LF3 checks for its validity in the database D2. If the OTP is found, the user is granted access.
