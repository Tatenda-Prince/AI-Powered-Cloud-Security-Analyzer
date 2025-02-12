# AI-Powered-Cloud-Security-Analyzer

"AI-Driven Threat Analysis"

# Technical Architecture

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/f59466dc8102f4d4f6b7074bb7686f82bf114548/img/Screenshot%202025-02-12%20141631.png)

## Project Overview

The CloudSentinel system automates cloud security monitoring by integrating AWS GuardDuty, Security Hub, Amazon Comprehend, AWS Lambda, and SNS. GuardDuty detects security threats and sends findings to Security Hub, which acts as a centralized security dashboard. The system stores logs in Amazon S3, where Amazon Comprehend performs AI-driven log analysis to identify suspicious patterns. AWS Lambda retrieves these insights, processes security alerts, and triggers notifications via Amazon SNS. Security admins receive real-time email alerts, allowing them to respond quickly to potential threats. This automated SecOps solution enhances AWS security by providing proactive threat detection and AI-powered analysis.

## Features

1.Continuous monitoring of AWS accounts and workloads.

2.Stores security logs in Amazon S3 for analysis.

3.Uses Amazon Comprehend (NLP AI) to detect anomalous security patterns in logs.

4.Lambda functions analyze security findings from Security Hub and Comprehend results.

5.Automates security event processing without human intervention.

6.Sends real-time notifications to Security Admins via Email or SMS.

7.Ensures faster incident response by alerting the right teams instantly.

## Prerequisites

1.AWS Account with an IAM User

2.Basic knowledge of the Python Programming Language

## Use Case 

You at the Up The Chels FinTech and you are tasked with detecting fraudulent transactions, phishing attempts, and unauthorized logins.


## Step 1: Set Up AWS GuardDuty

1.1.Log in to AWS Management Console.

Navigate to Amazon GuardDuty:

1.2.Search for "GuardDuty" in the AWS Management Console.

1.3.Enable GuardDuty:

1.4.Click on Get Started.

GuardDuty will automatically start analyzing VPC Flow Logs, CloudTrail events, and DNS logs.

Wait for Findings:

GuardDuty takes a few minutes to generate findings. You can check the Findings tab to see if any threats are detected.

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/4ceb267092588c66e3997bdc4445f22f93026859/img/Screenshot%202025-02-12%20143710.png)


## Step 2: Set Up AWS Security Hub

2.1.Go to AWS Security Hub:

Search for "Security Hub" in the AWS Management Console.

2.2.Enable Security Hub:

Click on Enable AWS Security Hub.

2.3Choose the default region (or the region where your resources are located).

Enable Security Standards:

2.4.In the Security Hub dashboard, go to Security Standards.

Enable AWS Foundational Security Best Practices.

Link GuardDuty to Security Hub:

2.5.Security Hub will automatically ingest findings from GuardDuty. You can view these findings in the Findings tab.

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/e2f08368181710fb9487bd4df7588a13cf11526a/img/Screenshot%202025-02-12%20144011.png)


## Step 3: Set Up Amazon Comprehend

3.1.Go to Amazon Comprehend:

Search for "Comprehend" in the AWS Management Console.

3.2.Prepare Log Data:

Upload a sample log file (e.g., CloudTrail logs) to an S3 bucket.

Example: Create a bucket named `tatenda-security-logs-bucket `and upload a `.txt ` file with sample log data.

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/5f0d8017d935ca535e6193023051b4190411333d/img/Screenshot%202025-02-12%20145303.png)


3.3.Create a Comprehend Analysis Job:

Go to Analysis Jobs and click Create Job.

Choose Custom Analysis.

Select the S3 bucket (`tatenda-security-logs-bucket`) as the data source.

Configure the job to detect `Entities and Key Phrases`.

Save the results in another S3 bucket (e.g., `tatenda-comprehend-results-bucket`).

3.4.Run the Job:

Start the analysis job and wait for it to complete.

Once done, check the results in the `tatenda-comprehend-results-bucket`.

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/6bdf46d7416190a2e105c9e811f022814c9ab21a/img/Screenshot%202025-02-12%20151150.png)


## Step 4: Create an AWS Lambda Function

4.1.Go to AWS Lambda:

Search for "Lambda" in the AWS Management Console.

Create a Lambda Function:

Click Create Function.

Choose Author from Scratch.

Name your function (e.g., SecurityAnalyzer).

Select Python 3.x as the runtime.

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/9e0439d0ec57672150de55da46828aac3664b689/img/Screenshot%202025-02-12%20151635.png)


4.2.Add Permissions:

Under Execution Role, choose Create a new role with basic Lambda permissions.

After creating the function, go to the IAM Console, find the role, and attach the following policies:

`AmazonGuardDutyReadOnlyAccess`

`AmazonSecurityHubReadOnlyAccess`

`AmazonS3ReadOnlyAccess`

`AmazonSNSFullAccess`

`ComprehendReadOnly`

4.3.Write the Lambda Code:

Replace the default code with the following Python script:

```python
import boto3

def lambda_handler(event, context):
    try:
        # Initialize clients
        guardduty = boto3.client('guardduty')
        securityhub = boto3.client('securityhub')
        comprehend = boto3.client('comprehend')
        sns = boto3.client('sns')

        # Fetch the DetectorId for GuardDuty
        detector_response = guardduty.list_detectors()
        if not detector_response['DetectorIds']:
            raise Exception("No GuardDuty Detector found in the account")
        detector_id = detector_response['DetectorIds'][0]

        # Fetch GuardDuty findings
        guardduty_findings = guardduty.list_findings(DetectorId=detector_id)
        for finding in guardduty_findings.get('FindingIds', []):
            print(f"GuardDuty Finding: {finding}")

        # Fetch Security Hub findings
        securityhub_findings = securityhub.get_findings()
        for finding in securityhub_findings.get('Findings', []):
            print(f"Security Hub Finding: {finding}")

        # Analyze logs with Comprehend
        comprehend_response = comprehend.detect_entities(
            Text="Sample log text", 
            LanguageCode="en"
        )
        for entity in comprehend_response.get('Entities', []):
            if entity['Type'] in ['PERSON', 'ORGANIZATION']:
                print(f"Suspicious Entity: {entity['Text']}")

        # Send alert via SNS
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:664418964175:SecurityAlerts',
            Message="Potential security threat detected!",
            Subject="Security Alert"
        )

        return {
            'statusCode': 200,
            'body': 'Security analysis completed!'
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
```

Replace the `TopicArn` with your SNS topic ARN (we’ll create this in the next step).

4.5.Deploy the Function:

Click Deploy to save the function.


## Step 5: Set Up Amazon SNS for Alerts

5.1.Go to Amazon SNS:

Search for "SNS" in the AWS Management Console.

5.2.Create an SNS Topic:

Click Create Topic.

Name your topic (e.g., `SecurityAlerts`).

Click Create Topic.

5.3.Subscribe to the Topic:

Select the topic and click Create Subscription.

Choose Email as the protocol and enter your email address.

Confirm the subscription by clicking the link in the confirmation email.

5.4.Get the Topic ARN:

Copy the ARN of the SNS topic (e.g., `arn:aws:sns:us-east-1:123456789012:SecurityAlerts`).

Update the TopicArn in the Lambda function with this value.


## Step 6: Test the Workflow

6.1.Trigger the Lambda Function:

Go to the Lambda function and click Test.

Create a new test event with the following JSON:

```language
json

{
  "key1": "value1",
  "key2": "value2"
}
```
Click Test to run the function.

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/19e4b4d27aa1313d38b6ded6352b991510cf6b30/img/Screenshot%202025-02-12%20153116.png)

6.2.Check the Output:

Go to the `CloudWatch Logs` for the Lambda function to see the execution logs.

Verify that the function fetches findings from GuardDuty and Security Hub.


Logs for GuardDuty

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/27a1325e1c66d9187b56928fe74d2ac0da9a787b/img/Screenshot%202025-02-12%20153249.png)


Security Hub

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/ea98c03e3f2acb99aef159822dd3e1e0e91bde2c/img/Screenshot%202025-02-12%20153305.png)




Check your email for the SNS alert.


![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Cloud-Security-Analyzer/blob/7cce1292b7e4341960627b1ddcee3253c050b5bb/img/Screenshot%202025-02-12%20153324.png)


## Congratulations

We have successfully created a "AI Cloud Security Analyzer" This project helped us understand AWS security services like GuardDuty, Security Hub, and SNS for real-time threat detection and response. We leveraged Amazon Comprehend for AI-powered log analysis and used AWS Lambda to automate security event processing. The serverless architecture ensured scalability and cost efficiency while reducing manual security monitoring efforts.


## Future Enhancements

To improve the system, we can integrate AWS Config for compliance monitoring, implement auto-remediation actions (e.g., blocking malicious IPs), and use Amazon OpenSearch for advanced security analytics.

























