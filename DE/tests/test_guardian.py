import pytest
from unittest.mock import MagicMock
import json
from src.main import get_guardian_article, send_to_sqs, get_or_create_queue, stream
from src.guardian_secrets import Secrets
from botocore.exceptions import ClientError

def test_get_guardian_article(mocker):
    mocker.patch("src.main.Secrets", autospec=True).return_value.get.return_value = "fake-key"
    fake_resp = mocker.Mock(status_code=200)
    fake_resp.json.return_value = {
        "response": {"results": [
            {"webPublicationDate": "2021-01-01", "webTitle": "Test", "webUrl": "http://example.com"}
        ]}
    }
    mocker.patch("requests.get", return_value=fake_resp)

    articles = get_guardian_article("anything", page_size=1)
    assert articles == [{
        "webPublicationDate": "2021-01-01",
        "webTitle": "Test",
        "webUrl": "http://example.com"
    }]

def test_send_to_sqs(mocker):
    mock_sqs = mocker.patch("boto3.client").return_value
    mock_sqs.send_message.return_value = {"MessageId": "abc"}
    send_to_sqs("url", {"foo": "bar"})
    mock_sqs.send_message.assert_called_once_with(
        QueueUrl="url",
        MessageBody=json.dumps({"foo": "bar"})
    )

def test_get_or_create_queue_existing(mocker):
    mock_sqs = mocker.patch("boto3.client").return_value
    mock_sqs.get_queue_url.return_value = {"QueueUrl": "https://sqs/123/exists"}
    url = get_or_create_queue("exists")
    assert url == "https://sqs/123/exists"

def test_get_or_create_queue_creation(mocker):
    expected = "https://sqs/123/new-queue"
    mock_sqs = mocker.patch("boto3.client").return_value
    mock_sqs.get_queue_url.side_effect = [
        ClientError({"Error": {"Code": "AWS.SimpleQueueService.NonExistentQueue"}}, "get_queue_url"),
        {"QueueUrl": expected}
    ]
    mock_sqs.create_queue.return_value = {"QueueUrl": expected}

    url = get_or_create_queue("new-queue")
    mock_sqs.create_queue.assert_called_once_with(QueueName="new-queue")
    assert url == expected

def test_stream_dry_run(mocker):
    mocker.patch("os.getenv", side_effect=lambda key, default=None: None)
    mocker.patch("src.main.Secrets", autospec=True).return_value.get.return_value = "fake-queue"
    mocker.patch("src.main.get_guardian_article", return_value=[
        {"webPublicationDate": "2021-01-01", "webTitle": "T", "webUrl": "U"}
    ])
    mocker.patch("src.main.send_to_sqs")
    echo = mocker.patch("typer.echo")

    stream(search_term="test", dry_run=True)

    echo.assert_any_call('DRY RUN -> {\n  "webPublicationDate": "2021-01-01",\n  "webTitle": "T",\n  "webUrl": "U"\n}')
