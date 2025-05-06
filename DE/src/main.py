import os
import requests
import json
import boto3
import typer
import logging
from typing import List, Dict, Optional
from botocore.exceptions import ClientError
from src.guardian_secrets import Secrets

logging.basicConfig(level=logging.INFO)
typer_log = logging.getLogger(__name__)

DEFAULT_REGION = "eu-west-2"


def get_guardian_article(
    q: str,
    date_from: Optional[str] = None,
    api_key: Optional[str] = None,
    page_size: int = 10,
) -> List[Dict]:
    """
    Query The Guardian API for articles matching the search term.
    """
    api_key = api_key or os.getenv("GUARDIAN_API_KEY") or Secrets().get("api_key")

    if not api_key:
        typer.echo("❌ Guardian API key missing.")
        raise typer.Exit(code=1)

    url = "https://content.guardianapis.com/search"
    params = {"q": q, "order-by": "newest", "page-size": page_size, "api-key": api_key}
    if date_from:
        params["from-date"] = date_from

    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        typer.echo(f"❌ Guardian API returned {resp.status_code}: {resp.text}")
        raise typer.Exit(code=1)

    data = resp.json()
    return [
        {
            "webPublicationDate": item.get("webPublicationDate"),
            "webTitle": item.get("webTitle"),
            "webUrl": item.get("webUrl"),
        }
        for item in data.get("response", {}).get("results", [])
    ]


def send_to_sqs(queue_url: str, message: dict, region_name: str = DEFAULT_REGION):
    """
    Send a message to the specified SQS queue.
    """
    sqs = boto3.client("sqs", region_name=region_name)
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
    typer_log.info(f"✅ Message sent! MessageId: {response.get('MessageId')}")


def get_or_create_queue(queue_name: str, region_name: str = DEFAULT_REGION) -> str:
    """
    Get the URL of an existing SQS queue or create a new one if it does not exist.
    """
    sqs = boto3.client("sqs", region_name=region_name)
    try:
        return sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "AWS.SimpleQueueService.NonExistentQueue":
            sqs.create_queue(QueueName=queue_name)
            return sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]
        raise


app = typer.Typer()


@app.command()
def stream(
    search_term: str = typer.Argument(..., help="Search keyword for The Guardian"),
    date_from: Optional[str] = typer.Option(
        None, "--date-from", "-d", help="Start date (YYYY-MM-DD)"
    ),
    page_size: int = typer.Option(
        10, "--page-size", "-n", help="Number of articles to retrieve"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Print results instead of sending to SQS"
    ),
):
    """
    Search The Guardian and stream articles to AWS SQS.
    """
    queue_name = os.getenv("SQS_QUEUE_NAME") or Secrets().get("queue_name")
    if not queue_name:
        typer.echo("❌ SQS queue name not found in environment or secrets.")
        raise typer.Exit(code=1)

    queue_url = get_or_create_queue(queue_name)

    articles = get_guardian_article(
        q=search_term, date_from=date_from, page_size=page_size
    )

    if not articles:
        typer.echo("⚠️ No articles found.")
        raise typer.Exit()

    for article in articles:
        message = {
            "webPublicationDate": article["webPublicationDate"],
            "webTitle": article["webTitle"],
            "webUrl": article["webUrl"],
        }
        if dry_run:
            # Print message without sending to SQS
            typer.echo(f"DRY RUN -> {json.dumps(message, indent=2)}")
        else:
            send_to_sqs(queue_url, message)
            typer.echo(f"✅ Sent: {article['webTitle']}")


if __name__ == "__main__":
    app()
