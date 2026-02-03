## Cloud Zero Trust Project (AWS)

A minimal AWS-based demonstration of Zero Trust Architecture principles

---

This project demonstrates a basic Zero Trust Architecture implementation on AWS using a containerized Flask application deployed on AWS Elastic Beanstalk. It showcases Zero Trust–style access between cloud services by enforcing least-privilege permissions and service-to-service trust only.

The project highlights:

🔐 Secure application deployment on AWS Elastic Beanstalk

🔄 Controlled EC2 → RDS database connectivity

📦 Secure file upload and download using Amazon S3

🚫 No public database access and no hardcoded credentials

---

# Architecture Overview

This project follows a Zero Trust–inspired cloud architecture, where every action is explicitly authorized, monitored, and logged.

  High-level flow:
  
  1. User accesses the Flask application deployed on AWS Elastic Beanstalk

  2. The application:
  
    Uploads / downloads files securely from Amazon S3
  
    Connects to Amazon RDS using restricted EC2 → RDS Security Group rules
  
  3. IAM roles are used for all AWS service access (no hardcoded credentials)
  
  4. AWS GuardDuty continuously monitors account activity
  
  5. On sensitive actions (such as API calls or uploads), GuardDuty generates findings
  
  6. Findings are delivered via Amazon SNS, which sends email notifications to the user

---

# Installation & Usage (End Users)

Open the Elastic Beanstalk application URL

Interact with the web UI to:

Upload files to S3

Download files from S3

Verify application response from the API

👉 No local setup required for end users.

---

## 🛠 Installation & Usage (For Contributors)

This section is for developers who want to **run, modify, or extend** the project locally.

---

###  Clone the Repository

```bash
git clone <your-repository-url>
cd cloud-zero-trust-project
```

---

### Install Dependencies

Make sure Python 3.8+ is installed.

```bash
pip install -r requirements.txt
```

---

### Run the Application Locally

```bash
python app.py
```

The application will start on:

```
http://localhost:5000
```

---

###  Build and Run Using Docker (Optional)

If you want to test the containerized setup:

```bash
docker build -t zero-trust-app .
docker run -p 5000:5000 zero-trust-app
```

---

### ☁️ AWS Configuration (For Cloud Testing)

To test AWS integrations (S3, RDS):

1. Configure AWS credentials:

   ```bash
   aws configure
   ```
2. Ensure your IAM user/role has permissions for:

   * S3
   * Elastic Beanstalk
   * EC2
   * RDS
3. Avoid using **root credentials**

---

## Zero Trust Concepts Demonstrated

* **Least privilege access**
* **Service-to-service trust only**
* **Private cloud networking**
* **Explicit access rules**
* **Identity-based permissions**

---

## Deployment Summary

* Application containerized using Docker
* Deployed using AWS Elastic Beanstalk
* AWS manages infrastructure provisioning securely

---

## Cleanup

To avoid AWS charges:

* Terminate Elastic Beanstalk environment
* Delete EC2, RDS, and S3 resources

---



