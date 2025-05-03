import os
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml 
# from google.oauth2 import service_account # For credentials


logger = get_logger(__name__)

# Path to your service account key JSON file # For local testing
# key_path = "/media/saawan/SAWAN HARD DISK/Projects/GCP/anime_recomender/inner-lightning-457510-s9-341a34702f47.json"

# Create credentials object # For local testing
# credentials = service_account.Credentials.from_service_account_file(key_path)

class DataIngestion:
    def __init__(self, config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.file_names = self.config['bucket_file_name']

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info("Data Ingestion initialized...........")


    def download_csv_from_gcp(self):
        try:
            # client = storage.Client(credentials=credentials) # For local testing
            client = storage.Client() # For production

            bucket = client.bucket(self.bucket_name)

            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR, file_name)

                if file_name == "animelist.csv":
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    data = pd.read_csv(file_path, nrows=5000000)
                    data.to_csv(file_path, index=False)
                    logger.info(f"Downloaded {file_name} from GCP bucket to {file_path} successfully.")

                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    logger.info("Downloaded the small file that is anime and anime with synopsis from GCP bucket to local directory.")
                    logger.info(f"Downloaded {file_name} from GCP bucket to {file_path} successfully.")

        except Exception as e:
            logger.error(f"Error downloading files from GCP bucket: {e}")
            raise CustomException("Error downloading files from GCP bucket", e)
        

    def run(self):
        try:
            logger.info("Starting data ingestion process...")
            self.download_csv_from_gcp()
            logger.info("Data ingestion process completed successfully.")
        except CustomException as ce:
            logger.error(f"Data ingestion process failed: {str(ce)}")
        finally:
            logger.info("Data ingestion process finished.")
        

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()



