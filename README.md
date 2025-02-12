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





