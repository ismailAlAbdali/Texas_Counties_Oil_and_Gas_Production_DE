if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
@transformer
def transform(dfs_dict, *args, **kwargs):
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
    'GP_COUNTY_DATA_TABLE' ,'OG_COUNTY_CYCLE_DATA_TABLE'

    DF_GP_DISTRICT_DATA_TABLE = pd.DataFrame(dfs_dict['GP_DISTRICT_DATA_TABLE'])
    DF_GP_COUNTY_DATA_TABLE = pd.DataFrame(dfs_dict['GP_COUNTY_DATA_TABLE'])
    DF_OG_COUNTY_CYCLE_DATA_TABLE = pd.DataFrame(dfs_dict['OG_COUNTY_CYCLE_DATA_TABLE'])

    # print(DF_GP_DISTRICT_DATA_TABLE) 
    DF_GP_COUNTY_DATA_TABLE = DF_GP_COUNTY_DATA_TABLE[["COUNTY_NO","COUNTY_NAME","COUNTY_FIPS_CODE","ON_SHORE_FLAG","ONSHORE_ASSC_CNTY_FLAG"]]
    
    # make some renames
    DF_GP_COUNTY_DATA_TABLE.rename(columns={'COUNTY_NO': 'COUNTY_ID'},inplace = True)
    # GP_DISTRICT Table
    DF_GP_DISTRICT_DATA_TABLE.rename(columns={'DISTRICT_NO': 'DISTRICT_ID'}, inplace=True)
    
    # let's add DATE_CYCLE_DIM table , and CNTY_PROD_DIM Table

    DATE_CYCLE_DIM = DF_OG_COUNTY_CYCLE_DATA_TABLE[["CYCLE_YEAR","CYCLE_MONTH","CYCLE_YEAR_MONTH"]]

    DATE_CYCLE_DIM["CYCLE_YEAR_MONTH_BIGN"] = pd.to_datetime(DATE_CYCLE_DIM["CYCLE_YEAR_MONTH"],format='%Y%m')
    DATE_CYCLE_DIM["MONTH_NAME"] = DATE_CYCLE_DIM["CYCLE_YEAR_MONTH_BIGN"].dt.month_name()
    # rearrange and drop duplicates
    DATE_CYCLE_DIM = DATE_CYCLE_DIM[["CYCLE_MONTH","MONTH_NAME","CYCLE_YEAR","CYCLE_YEAR_MONTH_BIGN","CYCLE_YEAR_MONTH"]].drop_duplicates()
    DATE_CYCLE_DIM["DATE_ID"] = DATE_CYCLE_DIM.index
    # Date Cycle Dim table
    DATE_CYCLE_DIM = DATE_CYCLE_DIM[["DATE_ID","CYCLE_MONTH","MONTH_NAME","CYCLE_YEAR","CYCLE_YEAR_MONTH_BIGN","CYCLE_YEAR_MONTH"]]

    # let's add the fact tabledf_gp_county
    OG_COUNTY_CYCLE_FACT = DF_OG_COUNTY_CYCLE_DATA_TABLE.drop(["COUNTY_NAME","DISTRICT_NAME","CYCLE_YEAR","CYCLE_MONTH"],axis = 1)
    OG_COUNTY_CYCLE_FACT = pd.merge(OG_COUNTY_CYCLE_FACT,DATE_CYCLE_DIM[['CYCLE_YEAR_MONTH', 'DATE_ID']], on='CYCLE_YEAR_MONTH', how='left')
    OG_COUNTY_CYCLE_FACT.drop(['CYCLE_YEAR_MONTH'],axis = 1,inplace = True)
    
    OG_COUNTY_CYCLE_FACT.rename(columns={'COUNTY_NO': 'COUNTY_ID', 'DISTRICT_NO': 'DISTRICT_ID'}, inplace=True)
    # OG_COUNTY_CYCLE_FACT TABLE
    ## now let's rearrange the table
    OG_COUNTY_CYCLE_FACT = OG_COUNTY_CYCLE_FACT[['COUNTY_ID','DISTRICT_ID','DATE_ID','CNTY_OIL_PROD_VOL','CNTY_GAS_PROD_VOL', 'CNTY_COND_PROD_VOL', 'CNTY_CSGD_PROD_VOL','OIL_GAS_CODE']]


    # print(df_us_counties)
    return {'OG_COUNTY_CYCLE_FACT': OG_COUNTY_CYCLE_FACT.to_dict(),
        'DATE_CYCLE_DIM' : DATE_CYCLE_DIM.to_dict(),
        'GP_COUNTY':DF_GP_COUNTY_DATA_TABLE.to_dict(),
        'GP_DISTRICT' : DF_GP_DISTRICT_DATA_TABLE.to_dict()
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
