import json
import boto3

BUCKET_NAME = "cloudtopia-images"
FACE_DETAILS_THRESHOLDS = {
    "Smile": {"desiredValue": False, "minConfidence": 90},
    "Sunglasses": {"desiredValue": False, "minConfidence": 90},
    "EyesOpen": {"desiredValue": True, "minConfidence": 90},
    "MouthOpen": {"desiredValue": False, "minConfidence": 90}
}

rekognition_client = boto3.client('rekognition')

def lambda_handler(event, context):
    current_file_name = event["Records"][0]["s3"]["object"]["key"]
    detect_faces_response = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': BUCKET_NAME, 'Name': current_file_name}},
        Attributes=['ALL']
    )
    face = detect_faces_response["FaceDetails"][0]
    parsed_response = {k: face[k] for k in FACE_DETAILS_THRESHOLDS.keys()}

    result = {"result": "PASS", "failure_reasons": []}
    for key, rule in FACE_DETAILS_THRESHOLDS.items():
        if parsed_response[key]["Value"] != rule["desiredValue"] or parsed_response[key]["Confidence"] < rule["minConfidence"]:
            result["result"] = "FAIL"
            result["failure_reasons"].append(key)

    print(json.dumps(result))
    return result
