if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

import zipfile
import os

def extract_and_delete_specific_files(zip_file_path, destination_directory, files_to_extract):

    """

    Extracts specific files from a zip archive and then deletes the archive.



    :param zip_file_path: Path to the zip file.

    :param destination_directory: Directory where files will be extracted.

    :param files_to_extract: List of filenames to be extracted from the zip file.

    """



    # Ensure the destination directory exists

    os.makedirs(destination_directory, exist_ok=True)



    # Unzip only the specified files

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:

        for file in files_to_extract:

            if file in zip_ref.namelist():

                zip_ref.extract(file, destination_directory)

                print(f"Extracted: {file}")

            else:

                print(f"File not found in the zip: {file}")



    print(f"Extracted selected files into: {destination_directory}")



    # Delete the zip file after extraction

    # if os.path.exists(zip_file_path):

    #     os.remove(zip_file_path)

    #     print(f"Deleted the zip file: {zip_file_path}")

    # else:

    #     print(f"File not found for deletion: {zip_file_path}")



@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here

    files_to_extract = [

    "GP_COUNTY_DATA_TABLE.dsv",

    "GP_DISTRICT_DATA_TABLE.dsv",

    "OG_COUNTY_CYCLE_DATA_TABLE.dsv"

]

    zip_file_name = "PDQ_DSV.zip"
    down_dir = "data_downloaded"

    # get zip file path
    zip_file_path = os.path.join(os.path.join(os.getcwd(),down_dir),zip_file_name)
    # get zip dest path
    dest_dir = os.path.join(os.getcwd(),"data")

    extract_and_delete_specific_files(zip_file_path,dest_dir,files_to_extract)

    return {}

