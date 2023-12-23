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
        'GP_DISTRICT_DATA_TABLE': 'https://storage.googleapis.com/county_prod_bucket_1/COUNTY_DATA/GP_DISTRICT_DATA_TABLE.dsv',
        'GP_COUNTY_DATA_TABLE': 'https://storage.googleapis.com/county_prod_bucket_1/COUNTY_DATA/GP_COUNTY_DATA_TABLE.dsv',
        'OG_COUNTY_CYCLE_DATA_TABLE': 'https://storage.googleapis.com/county_prod_bucket_1/COUNTY_DATA/OG_COUNTY_CYCLE_DATA_TABLE.dsv',
        'uscounties': 'https://storage.googleapis.com/county_prod_bucket_1/COUNTY_DATA/uscounties.csv'
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
    for key in dfs:
        dfs[key]['source'] = key

    combined_df = pd.concat(dfs.values(), ignore_index=True)
    return combined_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
