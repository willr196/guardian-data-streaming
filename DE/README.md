# Guardian Article Streamer

This is a Python project that searches for articles from The Guardian using their API and sends them to an AWS SQS queue. It can also just print out the articles if you don’t want to use AWS.

I made this while learning about APIs, AWS, secrets, and building command-line apps in Python. This README explains how to get it working, with a focus on keeping things simple.

## What it does

* Searches for Guardian articles based on a keyword.
* Sends each article to an AWS SQS queue, or prints them out if you're in dry run mode.
* Manages credentials using AWS Secrets Manager or a local .env file.

## Requirements

* Python 3.7 or higher
* A Guardian API key (you can register for free at the Guardian Open Platform)
* An AWS account
* AWS credentials (run `aws configure`) if you want to send data to SQS or use Secrets Manager
* Optional: AWS Secrets Manager (to store API keys and queue name securely)
* Optional: A .env file for local development

## Setup

1. Clone the repository and install dependencies.

Navigate into the project folder, create a virtual environment, activate it, and install the required packages.

2. Add your secrets

There are two ways to store your Guardian API key and queue name.

**Option A - Use AWS Secrets Manager:**
You can use the provided CLI script to create the secret. It stores both the Guardian API key and the SQS queue name in one secret.

Run:
`python src/create_secret.py --api-key "your-api-key" --queue-name "your-queue-name"`

This creates a secret called `guardian-project-secrets` in AWS. If the queue does not exist, it will also be created automatically when the app runs.

**Option B - Use a .env file:**
Create a file named `.env` in the project root, and add these lines:

```
GUARDIAN_API_KEY=your-api-key
SQS_QUEUE_NAME=your-queue-name
```

Make sure the `python-dotenv` package is installed so the app can read this file.

3. Configure AWS credentials (only if using SQS or Secrets Manager)

Run `aws configure` if you haven’t already. You’ll need access to SQS and optionally to Secrets Manager.

## Running the app

You can search for articles by keyword. The app will try to load your API key and queue name from Secrets Manager first. If that fails, it will fall back to the .env file.

Basic usage:
`python src/main.py stream "search term"`

Optional flags:

* `--date-from`: Filter by date (format YYYY-MM-DD)
* `--page-size`: Number of articles to fetch (default is 10)
* `--dry-run`: If set, articles are printed instead of sent to SQS

Example:
`python src/main.py "climate change" --date-from "2024-01-01" --page-size 5 --dry-run` While in the DE directory

If the SQS queue doesn’t exist yet, the app will create it automatically.

## Testing

You can run the tests using pytest.

Run:
`pytest`

to run all tests

To check code coverage, run:

```
coverage run -m pytest
coverage report
coverage html
```

## Code Quality

To check for code style and formatting issues, run:
`flake8 src`

To check for security issues, run:
`bandit -r src`

## Notes

You can use the app entirely in dry run mode if you don’t want to set up AWS.

The app always tries to use AWS Secrets Manager first. If that fails or isn’t set up, it will fall back to reading values from a .env file.

You only need AWS credentials and an actual SQS queue if you want to send articles to the cloud. Otherwise, everything else can be tested locally.

