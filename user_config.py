import os

# Default environment that will be used if none is specified (used in config_loader.py)
DEFAULT_ENVIRONMENT = 'local'

# File and directory names
DATA_DIRECTORY_NAME = 'data'
NEW_DRUG_APPROVALS_FILENAME = 'new_drug_approvals.csv'

# AWS Configuration (if running in an AWS environment)
AWS_BUCKET_NAME = 'app-new-drug-approvals-bucket'
AWS_SECRET_NAME = 'app-new-drug-approvals/environment-config'
AWS_REGION_NAME = 'us-east-1'