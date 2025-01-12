# AI Scheduling Agent

An AI scheduling agent using OpenAI Swarm that schedules meetings and can also send you personalized emails regarding scheduling tasks.

## Features

- Schedule meetings using Google Calendar
- Send personalized email invites
- Integrate with Calendly for scheduling
- Use Gradio for a user-friendly interface

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/AI_scheduling_agent.git
    cd AI_scheduling_agent
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your environment variables in the [.env] file:
    ```sh
    GOOGLE_APPLICATION_CREDENTIALS=client_secret.json
    GOOGLE_CALENDAR_DELEGATED_USER=your_delegated_user
    CALENDLY_PERSONAL_ACCESS_TOKEN=CALENDLY_PERSONAL_ACCESS_TOKEN
    CALENDLY_ORGANIZATION_ID=CALENDLY_ORGANIZATION_ID
    SENDGRID_API_KEY=SENDGRID_API_KEY
    MAIL_DEFAULT_SENDER=your_email
    MAIL_DEFAULT_SENDER_NAME=name
    OPENAI_API_KEY=OPENAI_API_KEY
    ```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. Open your browser and navigate to the URL provided by Gradio to interact with the AI scheduling agent.

## Using Docker

1. Build the Docker image:
    ```sh
    docker build -t ai_scheduling_agent .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 8000:8000 --env-file .env ai_scheduling_agent
    ```


## Example Videos

Here are two example videos demonstrating the usage of the AI scheduling agent:

1. Example Video 1
2. Example Video 2

## License

This project is licensed under the MIT License. See the LICENSE file for details.