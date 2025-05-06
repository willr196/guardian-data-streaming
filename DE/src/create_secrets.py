import boto3
import json
import argparse

def create_secret(secret_name, region_name, secret_value):
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        client.create_secret(Name=secret_name, SecretString=json.dumps(secret_value))
        print(f"Secret '{secret_name}' created.")
    except client.exceptions.ResourceExistsException:
        print(f"Secret '{secret_name}' already exists — updating it.")
        client.put_secret_value(SecretId=secret_name, SecretString=json.dumps(secret_value))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-key', required=True)
    parser.add_argument('--queue-name', required=True)
    args = parser.parse_args()

    create_secret(
        secret_name="guardian-project-secrets",
        region_name="eu-west-2",
        secret_value={
            "api_key": args.api_key,
            "queue_name": args.queue_name
        }
    )