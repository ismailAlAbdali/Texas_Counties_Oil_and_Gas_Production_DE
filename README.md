# Project Goal

## Overview
The primary goal of this project is to gain a some understanding of the **oil industry by analyzing data from the Railroad Commission of Texas**. Through this endeavor, we aim to achieve the following objectives:

### Explore Oil Industry Insights and Data Discovery
- Delve into the data to uncover valuable insights into the production of oil and gas over the years, providing a detailed understanding of production trends within the region. This process required data discovery and reading data catalogs to get some comprehensive understanding of the data.

### Learn Data Engineering
- This project serves as a learning opportunity to understand the intricacies of the data engineering process. By working on data collection, transformation, and visualization, we aim to acquire practical skills in data engineering.

### Leverage Modern Data Engineering Tools
- Embrace cutting-edge data engineering tools such as Mage-ai to streamline the ETL (Extract, Transform, Load) pipeline development. This enables us to work efficiently and effectively with complex data.

### Explore Google Cloud Computing
- Utilize the power of Google Cloud Computing for data storage and processing. This project provides hands-on experience with cloud-based solutions, enhancing our knowledge of cloud computing technologies.

### Automation in Python
- Learn to utilize python tools to automate manual weekly or monthly work in order to free up some time for more creative and productive endeavors.

# Basic Idea of the project:
- I have automated the daily process of extracting data from the RRC website through a data pipeline, exporting it to a cloud-based data lake, importing, modeling, and transferring it to a BigQuery data warehouse. Subsequently, I have utilized the Looker Studio data visualization platform for analytics. Periodic manual checks ensure the pipeline's smooth operation, but the majority of the workflow is fully automated and currently runs in weekly manner.

  

- Future work: make a sensor task ( task waits for an event) to download the data instead of downloading it weekly and not ensuring the data is updated or not. 

# Technology Stack

## Programming Languages and Tools
- Python: Utilized for data collection, transformation, and analysis.
- Jupyter Notebook: Used for interactive data exploration and documentation.
- Pandas: Employed for data manipulation and analysis.
- Selenium : Web Scraping tool to download data from a certain website.
- Chrome Webdriver manager: lets Selenium do its work.
- Google Cloud SDK: Write queries in the warehouse BigQuery and export data to cloud storage. 

## Google Cloud Platform (GCP)
- Google Storage: Utilized for data storage and accessibility.
- BigQuery: Leveraged for advanced data querying and analysis.
- Compute Engine: Used for scalable computing resources.
- Looker Studio: Applied for creating interactive and customized data visualizations.
- FireWall: Manage the IP Address that access Mage-AI server.

## Modern Data Pipeline Tool
- [Mage-ai](https://www.mage.ai/): A powerful and interactive open-source data engineering tool employed to streamline ETL (Extract, Transform, Load) pipelines. Mage-ai facilitates efficient data processing and transformation.

# Project Architecture

<img width="855" alt="image" src="https://github.com/ismailAlAbdali/Texas_Counties_Production_DE/assets/121197140/eb37f8e4-da92-459e-9d83-5e32baef0934">


# Data Model


<img width="938" alt="image" src="https://github.com/ismailAlAbdali/Texas_Counties_Production_DE/assets/121197140/5c3b462d-9e03-4f25-8c06-f0906193d44e">


**Data Collection**: Data was collected from the Texas Railroad Commission, ensuring the most accurate and up-to-date information. You can access the data directly from their website: [Texas Railroad Commission Data Sets](https://www.rrc.texas.gov/resource-center/research/data-sets-available-for-download/)

For additional information on the data, including a data dictionary and guidelines, please refer to the official user manual provided by the Texas Railroad Commission: [Data Dictionary and Guidelines](https://www.rrc.texas.gov/media/50ypu2cg/pdq-dump-user-manual.pdf)

# Data Pipeline Design:

![data-Pipeline](https://github.com/ismailAlAbdali/Texas_Counties_Production_DE/assets/121197140/cd739eda-c9ed-49ec-9005-b22a35b7781b)

Here is a description of DAG(Direct Acyclic Graph ) design showing what each task does in the pipeline.

| Task                     | Description of what it does                                                                                                            |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| `download_data`          | Downloads the data from the [Texas RRC](https://www.rrc.texas.gov/) website and then waits for the download to finish. Downloading the data takes about 20 minutes.                             |
| `unzip_data`               | After the data is downloaded, the `unzip_data` task is going to unzip the data so that it is ready to be exported to our cloud storage data lake.                                                   |
| `export_data_gcp`          | Exports the data into cloud storage.                                                                                                    |
| `load_data_from_gcp`       | After the data is exported, we load the data from the lake so it is ready to be transformed as designed in the data model.              |
| `clean_up_data`            | This process cleans up the data from the server so that it is ready for the next data downloading and loading, and also ensures we don't have extra storage in our local environment, keeping the server clean. |
| `transform_data`           | This task transforms the data from 3 DSV files scattered into 3 dim tables and 1 fact table so they are ready to be utilized in the data warehouse.                                              |
| `export_data_to_bigquery`  | Exports the data into the BigQuery data warehouse.                                                                                        |
| `run_analysis_prod_query`  | Runs DDL queries in order to make the data ready for analysis. All of the production data needed will be in our tables utilized for analysis.                                                    |


# Project Visualization:
Please Visit the Link to see the Dashboard of the data: [Texas Counties Oil and Gas production dashboard](https://lookerstudio.google.com/reporting/2feb4b80-a3f3-45e1-ac1a-9f11a1422634)


<img width="702" alt="image" src="https://github.com/ismailAlAbdali/Texas_Counties_Production_DE/assets/121197140/69cb0f2a-e891-460d-af63-8ab1727a1999">



# Questions or Feedback

If you have any questions, feedback, or suggestions regarding this project, please feel free to reach out. You can contact me at:

Email: [alabdaliesmail@gmail.com](mailto:alabdaliesmail@gmail.com)

Author: **Ismail Al Abdali**

I appreciate your input and am open to discussions, collaborations, and improvements. Don't hesitate to get in touch!


