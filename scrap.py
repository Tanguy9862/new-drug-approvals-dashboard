import logging
from datetime import datetime
from typing import Tuple

from flask import Flask, jsonify
import pandas as pd
from google.cloud import secretmanager
from new_drug_approvals_scraper.scraper import scrape_new_drug_approvals_data
import gcsfs

from config import (
    PROJECT_NAME,
    BUCKET_NAME,
    FILENAME,
    FILENAME_UPDATE,
    API_KEY_SECRET_ID
)


def access_secret_version(project_id, secret_id, version_id="latest"):
    """
    Access a secret version in Secret Manager.

    Args:
        project_id (str): Google Cloud project ID
        secret_id (str): Secret ID
        version_id (str): Version of the secret (default is "latest")

    Returns:
        str: The payload of the secret.
    """

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


app = Flask(__name__)


@app.route('/scrape_fda_approvals', methods=['GET'])
def scrape() -> Tuple:
    """
     Endpoint to trigger scraping of new FDA drug approvals.
     Scheduled to run every 6 hours via Google Cloud Scheduler.
     Updates the dataset stored on Google Cloud Storage and logs the update time.

     Returns:
         Tuple[json, int]: Response object with status and message, HTTP status code.
     """

    # Setup logging
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Read existing dataset from Google Cloud Storage
    gcs_path = f'gs://{BUCKET_NAME}/{FILENAME}'
    df = pd.read_csv(gcs_path)
    df['Date of Approval'] = pd.to_datetime(df['Date of Approval'], errors='coerce')

    # Retrieve the most recent date and drug name for incremental update
    most_recent_date, most_recent_drug = df.iloc[0]['Date of Approval'], df.iloc[0]['drug_name']

    try:
        # Call scraper function to get new data since the last update
        new_df = scrape_new_drug_approvals_data(
            openai_api_key=access_secret_version(project_id=PROJECT_NAME, secret_id=API_KEY_SECRET_ID),
            return_df=True,
            most_recent_date=most_recent_date,
            most_recent_drug=most_recent_drug
        )

    except Exception as e:
        logging.error("Error during scraping process", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

    else:
        # Update the dataset on Google Cloud Storage if new data is found
        if not new_df.empty:
            df_concatenated = pd.concat([new_df, df], ignore_index=True)
            df_concatenated.to_csv(gcs_path, index=False)
            logging.info("Data updated on Google Cloud Storage")

        # Update last execution time in a text file
        fs = gcsfs.GCSFileSystem(project=PROJECT_NAME)
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        file_path = f'gs://{BUCKET_NAME}/{FILENAME_UPDATE}'

        with fs.open(file_path, 'w') as f:
            f.write(now)
        logging.info(f"Last update timestamp written: {now}")

        return jsonify({"status": "success", "message": "Scraping completed"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
