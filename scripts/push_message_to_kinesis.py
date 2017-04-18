import boto3
import base64


def push():
    client = boto3.client('kinesis')

    msg = "This is message string"
    b64_msg = base64.encodestring(msg)

    response = client.put_record(StreamName='lambdaTestStream', Data=b64_msg, PartitionKey="partition4")

    print(str(response))

push()