# 🛂 CloudTopia: Passport Photo Validator

CloudTopia is a serverless AWS application that validates passport-style photos using Amazon Rekognition. It automatically checks if a face meets key criteria (no smile, eyes open, no sunglasses, mouth closed) and returns a PASS/FAIL result. The system is built with best practices in cloud architecture and demonstrates real-time, event-driven image analysis.

---

## 🌐 Live Scenario

When a user uploads an image to an S3 bucket:
- A Lambda function is triggered
- Rekognition analyzes the image
- The result is evaluated and stored in DynamoDB
- SNS sends notifications (optional)
- Users can retrieve results through a REST API via API Gateway

---

## 🧠 Architecture Overview

![CloudTopia Architecture](./architecture-diagram.pdf)

---

## ⚙️ AWS Services Used   

| Service             | Purpose                                                 |
|---------------------|----------------------------------------------------------|
| Amazon S3           | Stores uploaded passport images                         |
| AWS Lambda          | Processes images and returns validation results         |
| Amazon Rekognition  | Detects facial attributes (smile, sunglasses, etc.)     |
| Amazon DynamoDB     | Stores photo metadata and evaluation results            |
| Amazon SNS          | Sends notification after result is generated            |
| Amazon API Gateway  | Allows users to query results by image ID               |

---

## 🧩 Folder Structure

```
cloudtopia-passport-validator/
├── README.md
├── CloudTopia_Architecture.png
├── lambdas/
│   ├── rekognition-lambda.py      # Analyzes image and evaluates attributes
│   ├── dynamodb-lambda.py         # Writes validated results to DynamoDB
│   └── api-lambda.py              # Retrieves result via GET API
├── test-data/
│   └── sample-sns-event.json      # Sample trigger event from S3 upload
```

---

## 🔎 Features

- ✅ Automatically detects facial compliance with photo ID standards
- 🧠 Uses AI-powered analysis with Amazon Rekognition
- 🔄 Event-driven pipeline via S3 + Lambda
- 💾 Saves detailed results (pass/fail, reasons) to DynamoDB
- 🌐 Exposes a REST API to retrieve validation status
- 📨 Optional real-time notifications via SNS

---

## 🚀 Deployment Overview

1. Upload image to **S3** bucket
2. Triggers **Lambda → Rekognition**
3. Evaluates photo for:
   - Smile: ❌ Not allowed
   - Eyes Open: ✅ Required
   - Mouth Closed: ✅ Required
   - Sunglasses: ❌ Not allowed
4. Saves result to **DynamoDB**
5. Notifies via **SNS**
6. Query result via **API Gateway + Lambda**

---

## 🧪 Testing

You can simulate the workflow using the `sample-sns-event.json` file and trigger your Lambda manually through the AWS Console or CLI.

---

## 📈 Future Enhancements

- Add front-end photo upload form (React/S3 signed URLs)
- Add user authentication with Cognito
- Extend API with `/results/latest` and pagination
- Add CI/CD with GitHub Actions
- Add Unit Tests with pytest and moto

---

## 👨‍💻 Author

**Geoffrey Ninkyi**  
Cloud Solutions Architect | AWS Certified | Security-Focused Builder  
📍 Based in Virginia, USA  
🔗 [LinkedIn](#)

---

## 📬 Contact

For questions, issues, or collaboration:  
📧 Email: your-email@example.com  
📝 Open a GitHub issue or discussion

---

## 🛡️ License

This project is licensed under the MIT License.
