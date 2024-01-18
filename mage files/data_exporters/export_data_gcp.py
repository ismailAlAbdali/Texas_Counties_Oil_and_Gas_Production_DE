if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter



from google.cloud import storage
import zipfile
import os

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name,json_file):
    storage_client = storage.Client.from_service_account_json(json_file)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    # make the data public
    blob.make_public()
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

@data_exporter
def export_data(*args, **kwargs):
    """
    Sends data to the cloud storage using my google account crediential
    """
    # Specify your data exporting logic here

    bucket_name = "rrc-auto-extract"
    local_dir = "./data"
    account_json_file = "./file.json"
    
    for filename in os.listdir(local_dir):
        if ".dsv" in filename:
            upload_to_gcs(bucket_name,os.path.join(local_dir,filename),filename,account_json_file)
            print(f"Uploaded {filename} to {bucket_name}")
    

    print("Data has been exported successfully")


