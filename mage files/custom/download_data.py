if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os

download_url = "https://mft.rrc.texas.gov/link/1f5ddb8d-329a-4459-b7f8-177b4f5ee60d"
file_name_to_download = "PDQ_DSV.zip"

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except FileNotFoundError:
        return 0

@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here

    download_directory = os.path.join(os.getcwd(), "data_downloaded")
    os.makedirs(download_directory, exist_ok=True)

    def is_download_in_progress(directory):
        return any('.crdownload' in file for file in os.listdir(directory))

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # set dowbload and other conditions
    prefs = {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(download_url)
    print(driver.title)
    download_link = driver.find_element(By.LINK_TEXT, file_name_to_download)
    print("Downloading..,\n")
    download_link.click()


    # file_path = os.path.expanduser(download_directory)
    # print("Download completed or no .crdownload files found.")

    sleep(30)
    file_under_down_name = file_name_to_download + ".crdownload"

    file_under_down_path = os.path.join(download_directory,file_under_down_name)
    while is_download_in_progress(download_directory):
        current_size = get_file_size(file_under_down_path)
        print(f"{file_name_to_download} file is currently downloading ... size downloaded = {current_size}")

        sleep(20) # sleep for 20 seconds -> only want to stall for the program to be running until the download finishes. 

    full_size = get_file_size(os.path.join(download_directory,file_name_to_download))
    print("file {file_name_to_download} size = {full_size}")
    return {}




@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'