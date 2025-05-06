import pytest
from unittest.mock import patch, MagicMock
from src.guardian_secrets import Secrets
import json
from botocore.exceptions import ClientError



def test_get_secrets_success():
    with patch("boto3.client") as mock_client:
        mock_secrets = {
            "api_key": "fake-api-key",
            "queue_name": "fake-queue-name"
        }
        mock_response = MagicMock()
        mock_response.get_secret_value.return_value = {
            "SecretString": json.dumps(mock_secrets)
        }
        mock_client.return_value = mock_response
        secrets = Secrets(secret_name="guardian-project-secrets", region_name="eu-west-2")
        assert secrets.get("api_key") == "fake-api-key"
        assert secrets.get("queue_name") == "fake-queue-name"


def test_get_secrets_failure():
    with patch("boto3.client") as mock_client:
        mock_response = MagicMock()
        mock_client.return_value = mock_response
        mock_response.get_secret_value.side_effect = ClientError(
            {"Error": {"Code": "AccessDeniedException", "Message": "Access Denied"}},
            "get_secret_value"
        )
        with pytest.raises(RuntimeError, match="Unable to load secrets"):
            Secrets(secret_name="guardian-project-secrets", region_name="eu-west-2")