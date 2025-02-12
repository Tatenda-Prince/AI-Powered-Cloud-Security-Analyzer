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
