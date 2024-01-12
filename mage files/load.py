import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    
    urls = {
        'GP_DISTRICT_DATA_TABLE': 'https://storage.googleapis.com/rrc-auto-extract/GP_DISTRICT_DATA_TABLE.dsv',
        'GP_COUNTY_DATA_TABLE': 'https://storage.googleapis.com/rrc-auto-extractGP_COUNTY_DATA_TABLE.dsv',
        'OG_COUNTY_CYCLE_DATA_TABLE': 'https://storage.googleapis.com/rrc-auto-extractOG_COUNTY_CYCLE_DATA_TABLE.dsv',
    }
    dfs = {}

    for key, value in urls.items():
        response = requests.get(value)
        if response.status_code == 200:
            if '.dsv' in value:
                dfs[key] = pd.read_csv(io.StringIO(response.text), delimiter="}", low_memory=False)
            else:
                dfs[key] = pd.read_csv(io.StringIO(response.text), sep=',')
        else:
            print(f"Failed to load data from {value}")

        # Adding an identifier column to each DataFrame
    return {
        'GP_DISTRICT_DATA_TABLE' :  dfs['GP_DISTRICT_DATA_TABLE'].to_dict(),
       'GP_COUNTY_DATA_TABLE' :  dfs['GP_COUNTY_DATA_TABLE'].to_dict(),
        'OG_COUNTY_CYCLE_DATA_TABLE' :  dfs['OG_COUNTY_CYCLE_DATA_TABLE'].to_dict()
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
