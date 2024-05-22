import boto3
from django.conf import settings
from main.models import *
from django.utils import timezone


# Configure SES client with credentials from settings.py
ses_client = boto3.client(
    'ses',
    region_name=settings.AWS_SES_REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)



def send_welcome_email(to_email):
    try:
        # Retrieve email body from Email_Body table
        email_body = Email_Body.objects.get(email_type='WELCOME_MAIL')

        # Retrieve user details from the User and Profile tables
        user = User.objects.get(email=to_email)
        profile = Profile.objects.get(user=user)

        # Render email subject and body with user details
        subject = email_body.subject
        body = email_body.body.format(
            username=user.username,
            first_name=profile.first_name,
            last_name=profile.last_name,
            email=profile.email
        )

        # Send email using SES
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [to_email],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source="infiniteedulocus@gmail.com"
        )

        # Log email sending status in the Email_Log table
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            # Email sent successfully
            EmailLog.objects.create(
                email_type=email_body.email_type,
                status='Success',
                reason=None,
                datetime=timezone.now(),
                user_email=to_email
            )
        else:
            # Failed to send email
            EmailLog.objects.create(
                email_type=email_body.email_type,
                status='Error',
                reason=response['Error']['Message'],
                datetime=timezone.now(),
                user_email=to_email
            )
    except Exception as e:
        # Log exception in the Email_Log table
        EmailLog.objects.create(
            email_type='WELCOME_MAIL',
            status='Error',
            reason=str(e),
            datetime=timezone.now(),
            user_email=to_email
        )
