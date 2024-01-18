if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


from google.cloud import bigquery

@custom
def run_analysis_prod_query(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    
    client = bigquery.Client.from_service_account_json("./rail-road-texas-og-county-prod-15d38d72a0da.json")
    prod_query = """CREATE OR REPLACE TABLE `rail-road-texas-og-county-prod.CountyProdOG.COUNTY_PROD_ANALYSIS` AS ( select DIS.DISTRICT_NAME, GP_C.COUNTY_NAME, CONCAT('48', LPAD(CAST(GP_C.COUNTY_FIPS_CODE AS STRING), 3, '0'))AS COUNTY_FIPS_CODE, D.CYCLE_MONTH, D.MONTH_NAME, D.CYCLE_YEAR, D.CYCLE_YEAR_MONTH, D.CYCLE_YEAR_MONTH_BIGN, CO.CNTY_OIL_PROD_VOL, CO.CNTY_GAS_PROD_VOL, CO.CNTY_COND_PROD_VOL, CO.CNTY_CSGD_PROD_VOL, CO.OIL_GAS_CODE from `rail-road-texas-og-county-prod.CountyProdOG.OG_COUNTY_CYCLE_FACT` CO join `rail-road-texas-og-county-prod.CountyProdOG.GP_COUNTY` GP_C on CO.COUNTY_ID = GP_C.COUNTY_ID join `rail-road-texas-og-county-prod.CountyProdOG.DATE_CYCLE_DIM` D on CO.DATE_ID = D.DATE_ID join `rail-road-texas-og-county-prod.CountyProdOG.GP_DISTRICT` DIS on CO.DISTRICT_ID = DIS.DISTRICT_ID );"""
    query_job  = client.query(prod_query).result()
    

    print("Done making COUNTY_PROD_ANALYSIS Table... Ready for data Analysis")
    return {}

