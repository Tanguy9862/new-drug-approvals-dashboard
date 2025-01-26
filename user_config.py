import os

# Default environment that will be used if none is specified (used in config_loader.py)
DEFAULT_ENVIRONMENT = 'local'

# File and directory names
DATA_DIRECTORY_NAME = 'data'
NEW_DRUG_APPROVALS_FILENAME = 'new_drug_approvals.csv'

# GCP Configuration (if running in a GCP environment)
GCP_PROJECT_ID = 'new-drug-approvals'
GCP_BUCKET_NAME = 'new-drug-approvals-bucket'
GCP_SECRET_NAME = 'new-drug-approvals-config'  # The name of the secret in GCP Secret Manager, used to store the
# environment configuration (e.g., ENV=gcp)

# Local configuration to access GCP resources (only for development/testing)
# This sets the path to the service account key JSON file for authentication.
# If None, GCP authentication will rely on the default application credentials (ADC).
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'new-drug-approvals-4093ccdb6f83.json' or None