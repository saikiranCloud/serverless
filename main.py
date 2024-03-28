import base64,json,requests,os,traceback
from datetime import datetime
import functions_framework
from dotenv import load_dotenv
import urllib.parse
from sqlalchemy import create_engine,text
load_dotenv()

db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_host = os.environ['DB_HOST']
mailgun_domain = os.environ['MAILGUN_DOMAIN']
mailgun_api = os.environ['MAILGUN_API_KEY'] 

# db_user="cloudsql_user"
# db_password="G-2PfScB6JvTt)kq"
# db_name="cloudsql_database"
# db_host="172.30.0.8"
# mailgun_domain = "saikirankolloju.me"
# mailgun_api = "e5be0622dd99e810d8aec9b742fa64f2-f68a26c9-a1aa21e6"


engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/")
with engine.connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    connection.execute(text(f"USE {db_name}"))

# query = "SELECT * FROM your_table"
# result = connection.execute(query)

html_template = """
<!DOCTYPE html>
<html lang="en">
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Verification Email for User Creation</title>
   </head>
   <body>
      <p>Hello,</p>
      <p>Please click the following link to verify your email address:</p>
      <a href="{verification_link}">Verify Email</a>
   </body>
</html>
"""

def generate_verification_link(verification_token):
    base_url = f"http://{mailgun_domain}:5000/v1/user/verify"
    params = {"verify_token": verification_token}
    link = base_url + "?" + urllib.parse.urlencode(params)
    return link

def track_email_sent(email):
    with engine.connect() as connection:
        update_query = text("UPDATE user_data SET mail_sent = :mail_sent, mail_sent_time = :mail_sent_time WHERE email = :email")
# Execute the update query with parameters
        connection.execute(update_query, email=email, mail_sent=True, mail_sent_time=datetime.now())
        print("Email sent status updated successfully.")

def send_verification_email(email, verification_link):
    def send_html_message(html_content):
        return requests.post(
            "https://api.mailgun.net/v3/{}/messages".format(mailgun_domain),
            auth=("api", mailgun_api),
            data={"from": "support@{}".format(mailgun_domain),
                  "to": [email],
                  "subject": "Verification Email",
                  "html": html_content})
    html_content = html_template.format(verification_link=verification_link)
    response = send_html_message(html_content)
    if response.status_code == 200:
        print("Email sent successfully!")
        track_email_sent(email)
    else:
        print(f"Failed to send email. Status code: {response.status_code}")


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    print("sfdsf",base64.b64decode(cloud_event.data["message"]["data"]))
    try:
        # Decode the Pub/Sub message data
        pubsub_message = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
        message = json.loads(pubsub_message)
        print(message)
        print("sgdg",type(message))
        # Extract email and verification link from the message
        email = message["email"]
        verification_token = message["verification_token"]
        verification_link = generate_verification_link(verification_token)
        print("verlink",verification_link)
        send_verification_email(email, verification_link)
        print("Email verification sent and tracked successfully")
    except Exception as e:
        # Using traceback to get full error details
        traceback_details = traceback.format_exc()
        print("Full error details:")
        print(traceback_details)