import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(combined_df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    
    # let's lets dustrcut the data and put it into four different dataframes.
    separated_dfs = {}

    # The unique identifiers for the original DataFrames
    sources = combined_df['source'].unique()

    # Separating the combined DataFrame
    for source in sources:
        separated_dfs[source] = combined_df[combined_df['source'] == source].drop('source', axis=1)

    # get the data seperated and clean and the NANs
    df_district = separated_dfs['GP_DISTRICT_DATA_TABLE'].dropna(axis = 1)
    df_gp_county = separated_dfs['GP_COUNTY_DATA_TABLE'].dropna(axis = 1)
    df_og_county_cycle = separated_dfs['OG_COUNTY_CYCLE_DATA_TABLE'].dropna(axis = 1)
    df_us_counties = separated_dfs['uscounties'].dropna(axis = 1)
    


    # get all Texaes State counties information
    cond2 = df_us_counties["state_id"] == "TX" # we only need state_id = 'TX'
    df_us_counties_Teaxes = df_us_counties[cond2]
    df_us_counties_Teaxes['county'] = df_us_counties_Teaxes['county'].apply(lambda x: str.upper(x)) # make all upper cases county names

    county_mapping = df_us_counties_Teaxes.set_index('county')[['lat','lng']] # get the county location mapping

    df_gp_county.drop(["DISTRICT_NO","DISTRICT_NAME"] ,axis = 1,inplace=True) # drop columns : "DISTRICT_NO","DISTRICT_NAME"

    df_gp_county["COUNTY_LATITUDE"] = df_gp_county["COUNTY_NAME"].map(county_mapping['lat']) # adding latitude column
    df_gp_county["COUNTY_LONGITUDE"] = df_gp_county["COUNTY_NAME"].map(county_mapping['lng']) ## addint longitude column

    df_gp_county = df_gp_county[["COUNTY_NO","COUNTY_NAME","COUNTY_LATITUDE","COUNTY_LONGITUDE","COUNTY_FIPS_CODE","ON_SHORE_FLAG","ONSHORE_ASSC_CNTY_FLAG"]]
    
    # make some renames
    df_gp_county.rename(columns={'COUNTY_NO': 'COUNTY_ID'},inplace = True)
    # GP_DISTRICT Table
    df_district.rename(columns={'DISTRICT_NO': 'DISTRICT_ID'}, inplace=True)


    # make some fuxed in couting table
    
    # let's add DATE_CYCLE_DIM table , and CNTY_PROD_DIM Table

    DATE_CYCLE_DIM = df_og_county_cycle[["CYCLE_YEAR","CYCLE_MONTH","CYCLE_YEAR_MONTH"]]
    DATE_CYCLE_DIM["CYCLE_YEAR_MONTH_BIGN"] = pd.to_datetime(DATE_CYCLE_DIM["CYCLE_YEAR_MONTH"],format='%Y%m')
    DATE_CYCLE_DIM["MONTH_NAME"] = DATE_CYCLE_DIM["CYCLE_YEAR_MONTH_BIGN"].dt.month_name()
    # rearrange and drop duplicates
    DATE_CYCLE_DIM = DATE_CYCLE_DIM[["CYCLE_MONTH","MONTH_NAME","CYCLE_YEAR","CYCLE_YEAR_MONTH_BIGN","CYCLE_YEAR_MONTH"]].drop_duplicates()
    DATE_CYCLE_DIM["DATE_ID"] = DATE_CYCLE_DIM.index
    # Date Cycle Dim table
    DATE_CYCLE_DIM = DATE_CYCLE_DIM[["DATE_ID","CYCLE_MONTH","MONTH_NAME","CYCLE_YEAR","CYCLE_YEAR_MONTH_BIGN","CYCLE_YEAR_MONTH"]]

    # let's add the fact table
    OG_COUNTY_CYCLE_FACT = df_og_county_cycle.drop(["COUNTY_NAME","DISTRICT_NAME","CYCLE_YEAR","CYCLE_MONTH"],axis = 1)
    OG_COUNTY_CYCLE_FACT = pd.merge(OG_COUNTY_CYCLE_FACT,DATE_CYCLE_DIM[['CYCLE_YEAR_MONTH', 'DATE_ID']], on='CYCLE_YEAR_MONTH', how='left')
    OG_COUNTY_CYCLE_FACT.drop(['CYCLE_YEAR_MONTH'],axis = 1,inplace = True)
    
    OG_COUNTY_CYCLE_FACT.rename(columns={'COUNTY_NO': 'COUNTY_ID', 'DISTRICT_NO': 'DISTRICT_ID'}, inplace=True)
    # OG_COUNTY_CYCLE_FACT TABLE
    ## now let's rearrange the table
    OG_COUNTY_CYCLE_FACT = OG_COUNTY_CYCLE_FACT[['COUNTY_ID','DISTRICT_ID','DATE_ID','CNTY_OIL_PROD_VOL',
       'CNTY_GAS_PROD_VOL', 'CNTY_COND_PROD_VOL', 'CNTY_CSGD_PROD_VOL','OIL_GAS_CODE']]


    # print(df_us_counties)
    return {'OG_COUNTY_CYCLE_FACT': OG_COUNTY_CYCLE_FACT.to_dict(),
        'DATE_CYCLE_DIM' : DATE_CYCLE_DIM.to_dict(),
        'GP_COUNTY':df_gp_county.to_dict(),
        'GP_DISTRICT' : df_district.to_dict()
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
