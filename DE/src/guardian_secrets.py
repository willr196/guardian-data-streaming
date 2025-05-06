import boto3
import json
from botocore.exceptions import ClientError

class Secrets:
    def __init__(self, secret_name='guardian-project-secrets', region_name="eu-west-2"):
        self.secret_name = secret_name
        self.region_name = region_name
        self._secrets = self._get_secrets()

    def _get_secrets(self):
        client = boto3.client('secretsmanager', region_name=self.region_name)
        try:
            response = client.get_secret_value(SecretId=self.secret_name)
            secret_str = response.get('SecretString')
            return json.loads(secret_str)
        except ClientError as e:
            raise RuntimeError(f"Unable to load secrets: {e}")

    def get(self, key):
        return self._secrets.get(key)



