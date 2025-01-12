from google_apis import construct_google_credentials
from sendgrid.helpers.mail import Mail, Email, To, Content
import requests
from datetime import datetime
import sendgrid
from google.auth.transport import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.apps import meet_v2
from dotenv import load_dotenv
import os
################################################# Tool Creation###########################################################""
def list_events(time_min: str, time_max: str) -> dict:
    """List all events in a calendar
    :param time_min: The minimum time to list events as a datetime string (ie. '2022-01-01T00:00:00Z')
    :param time_max: The maximum time to list events as a datetime string (ie. '2022-01-01T00:00:00Z')
    """
    service = build('calendar', 'v3', credentials=credentials)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        return {'message': 'No events found.'}

    return {'events': events}

def create_event(summary: str, description: str, start_time: str, end_time: str) -> dict:
    """Create a new event in a calendar.
    :param summary: The event summary
    :param description: The event description
    :param start_time: The start time of the event as a datetime string (ie. '2024-01-01T00:00:00Z')
    :param end_time: The end time of the event as a datetime string (ie. '2024-01-01T00:00:00Z')
    """
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event



def get_event(event_id: str) -> dict:
    """Get an event by ID.
    :param event_id: The ID of the event
    """
    service = build('calendar', 'v3', credentials=credentials)

    event = service.events().get(calendarId='primary', eventId=event_id).execute()

    return event


def update_event(event_id: str, summary: str, description: str, start_time: str, end_time: str) -> dict:
    """Update an event.
    :param event_id: The ID of the event
    :param summary: The event summary
    :param description: The event description
    :param start_time: The start time of the event as a datetime string (ie. '2022-01-01T00:00:00Z')
    :param end_time: The end time of the event as a datetime string (ie. '2022-01-01T00:00:00Z')
    """
    service = build('calendar', 'v3', credentials=credentials)
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'UTC',
        },
    }
    event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()

    return event


def delete_event(event_id: str) -> dict:
    """Delete an event.
    :param event_id: The ID of the event
    """
    service = build('calendar', 'v3', credentials=credentials)

    service.events().delete(calendarId='primary', eventId=event_id).execute()

    return {
        'message': 'Event deleted.'
    }







def send_invite_email(to_email: str, calendly_link='https://calendly.com/your-calendly') -> dict:
    """Send a personalized email using SendGrid.
    :param to_email: The email address to send the invite to
    :param calendly_link: The Calendly link to include in the email
    """

    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(email=os.environ.get('MAIL_DEFAULT_SENDER'), name=os.environ.get('MAIL_DEFAULT_SENDER_NAME'))

    subject = "Let's Schedule a Meeting 📅"

    # Set up the HTML email content with a styled button
    content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
        <style>
            html {{
                background-color: #f9fafb;
            }}
            body {{
                font-family: 'Inter', sans-serif;
                color: #000000;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3 {{
                color: #15803d;
                font-family: 'Inter', sans-serif;
            }}
            p, ul {{
                line-height: 1.5;
            }}
            a {{
                color: #fff;
                text-decoration: none;
                font-weight: 600;
                margin: 24px 0;
            }}
            .btn {{
                display: inline-block;
                background-color: #15803d;
                color: #fff;
                padding: 10px 20px;
                border-radius: 5px;
                text-align: center;
                text-decoration: none;
            }}
            .ii a[href] {{
                color: #fff !important;
                text-decoration: none;
                font-weight: 600;
                margin: 24px 0;
            }}
            p {{ margin: 0; padding: 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div style="margin-top: 50px;">
            <h2>Let's Schedule a Meeting</h2>
            <p>Let's set up a time to chat. You can schedule a meeting with me using the button below:</p>
            <p><a href="{calendly_link}" class="btn">Schedule a Meeting</a></p>
            <p>If you did not request this email, please ignore it.</p>
            <p>Best regards,<br>
            {from_email.name}</p>
            <br/>
            <p style="font-size: 12px">
                If you’re having trouble clicking the "Schedule a Meeting" button, copy and paste the URL below into your web browser:
                <br>
                <a href="{calendly_link}">{calendly_link}</a>
            </p>
        </div>
        </div>
    </body>
    </html>
    """

    message = Mail(
        from_email=from_email,
        to_emails=To(to_email),
        subject=subject,
        html_content=Content("text/html", content.strip())
    )

    sg.send(message)

    return {
        'message': 'Email sent.'
    }



def get_google_meet_link() -> dict:
    """Get a Google Meet link."""
    client = meet_v2.SpacesServiceClient(credentials=credentials)
    request = meet_v2.CreateSpaceRequest()
    response = client.create_space(request)

    return {
        'message': 'Google Meet link created.',
        'meeting_uri': response.meeting_uri
    }


api_key=os.environ.get("OPENAI_API_KEY")
credentials = construct_google_credentials()