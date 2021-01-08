import json
import os
import boto3
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
translated = boto3.client('translate')
comprehend = boto3.client('comprehend')


def translete(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all todos from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    target = event['pathParameters']['language']
    task =  result['Item']['text']
    source_lenguage = detect_language(task)
    
    source = source_lenguage['Languages'][0]['LanguageCode']
    
    response = translate_text(task, source, target)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response

def detect_language(task):
    response = comprehend.detect_dominant_language(Text=task)
    return response

def translate_text(task, source, target):
    
    response = translated.translate_text(Text=task, SourceLanguageCode=source , TargetLanguageCode=target)
    
    return response