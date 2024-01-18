if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

import os
import shutil

def delete_folder_contents(folder):
    """ Deletes the contents of the specified folder. """
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here

    # Folder names
    folders = ['data', 'data_downloaded']

    # Delete contents of each folder
    for folder in folders:
        delete_folder_contents(folder)
        print(f"Contents of '{folder}' have been deleted.")

    return {}

