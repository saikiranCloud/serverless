# serverless

## Verification Email Functionality
This code implements a function for sending verification emails to users for email address verification upon user creation. It is designed to be triggered by a message on a Cloud Pub/Sub topic.

# Prerequisites
Before running this code, ensure you have the following set up:

MySQL Database: Set up a MySQL database to store user data, including email addresses and verification status.
Mailgun Account: Obtain API credentials (API key and domain) from Mailgun for sending emails.
Cloud Pub/Sub Topic: Set up a Cloud Pub/Sub topic to trigger the function.
Configuration
The following environment variables need to be set:

DB_USER: MySQL database username.
DB_PASSWORD: MySQL database password.
DB_NAME: MySQL database name.
DB_HOST: MySQL database host.
MAILGUN_DOMAIN: Mailgun domain for sending emails.
MAILGUN_API_KEY: Mailgun API key for authentication.

# Functionality
1. Database Setup
The code connects to the MySQL database and creates the necessary tables if they do not exist. It uses SQLAlchemy to interact with the database.

2. Email Template
The HTML template for the verification email is defined in the html_template variable. It contains placeholders for the verification link.

3. Email Sending
The send_verification_email function sends the verification email using the Mailgun API. It constructs the HTML content of the email using the provided template and includes the verification link.

4. Verification Link Generation
The generate_verification_link function generates the verification link based on the verification token. It constructs the link using the base URL and appends the token as a query parameter.

5. Email Tracking
The track_email_sent function updates the database to track the status of email delivery. It marks the email as sent and records the timestamp.

6. Pub/Sub Trigger
The hello_pubsub function is triggered by messages on a Cloud Pub/Sub topic. It decodes the message, extracts the email address and verification token, generates the verification link, sends the verification email, and tracks the email delivery status.

# Usage
Set up the required environment variables.
Deploy the function to a cloud environment (e.g., Google Cloud Functions) and ensure it is configured to be triggered by a Cloud Pub/Sub topic.
Publish messages to the Cloud Pub/Sub topic with the required payload (email address and verification token) to trigger the function.
Notes
Ensure proper error handling and logging to handle failures gracefully and monitor the execution of the function.
Test the functionality thoroughly, including email delivery and database updates, to ensure reliability and correctness.
