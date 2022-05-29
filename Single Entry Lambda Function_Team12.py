import boto3
from urllib import request
import json


aws_access_id = "AKIATX6QVFRR324QDABL"
aws_secret_access_key = "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"
sqs = boto3.client("sqs", region_name='us-east-1', aws_access_key_id=aws_access_id,
                   aws_secret_access_key=aws_secret_access_key)
def send_sqs_message(sqs_queue_url, msg_body):
    """

    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_body: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    # Send the SQS message
    #sqs_client = boto3.client('sqs')


    msg = sqs.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=json.dumps(msg_body), MessageGroupId='123')

    return msg

def lambda_handler(event, context):

        msg= event['body']
        if msg['type']=='text':
            queue_url = 'https://sqs.us-east-1.amazonaws.com/257598762083/textanalysis.fifo'
            response=send_sqs_message(queue_url, msg['content'])

            print(response)
            if msg['content'] is not None:
                #logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
                return {
                    'statusCode': 200,
                    'body': json.dumps(msg['content'])
                }
            else:
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'error': 'No review provided'
                    })
                }

        
        else:
                img = event['body']

                queue_url = 'https://sqs.us-east-1.amazonaws.com/257598762083/Imageanalysis.fifo'
                response = send_sqs_message(queue_url, img['content'])

                print(response)
                if img['content'] is not None:
                    # logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
                    return {
                        'statusCode': 200,
                        'body': json.dumps(img['content'])
                    }
                else:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({
                            'error': 'No review provided'
                        })
                    }
