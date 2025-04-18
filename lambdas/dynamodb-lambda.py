import json
import boto3
import datetime

BUCKET_NAME = "cloudtopia-images"
FACE_DETAILS_THRESHOLDS = {
    "Smile": {"desiredValue": False, "minConfidence": 90},
    "Sunglasses": {"desiredValue": False, "minConfidence": 90},
    "EyesOpen": {"desiredValue": True, "minConfidence": 90},
    "MouthOpen": {"desiredValue": False, "minConfidence": 90}
}

rekognition_client = boto3.client('rekognition')
dynamodb_client = boto3.resource('dynamodb')
validation_table = dynamodb_client.Table('ValidationRequests')

def lambda_handler(event, context):
    file_name = event["Records"][0]["s3"]["object"]["key"]
    faces = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': file_name}},
        Attributes=['ALL']
    )
    face = faces["FaceDetails"][0]
    face_data = {k: face[k] for k in FACE_DETAILS_THRESHOLDS.keys()}
    
    result = {"result": "PASS", "failure_reasons": []}
    for key, rule in FACE_DETAILS_THRESHOLDS.items():
        if face_data[key]["Value"] != rule["desiredValue"] or face_data[key]["Confidence"] < rule["minConfidence"]:
            result["result"] = "FAIL"
            result["failure_reasons"].append(key)

    validation_table.put_item(Item={
        'FileName': file_name,
        'ValidationResult': result["result"],
        'FailureReasons': json.dumps(result["failure_reasons"]),
        'Timestamp': datetime.datetime.now().replace(microsecond=0).isoformat(),
        'FileLocation': f"{BUCKET_NAME}/{file_name}",
        'FaceDetails': json.dumps(face_data)
    })

    return result
