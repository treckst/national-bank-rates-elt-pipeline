# national-bank-rates-elt-pipeline
Automated cloud ELT-pipeline for data ingestion using Azure Function (Time-Trigger) and Microsoft Fabric.

It's a project that automates the ingestion, transformation, and storage of data from the National Bank of Poland API (https://api.nbp.pl/).

It shows a power of cloud architecture using Azure and Microsoft Fabric with Bronze and Silver layers.

# Extraction: Python Azure Function (Timer-Trigger) fetches every 5min for exchange rates and gold prices in JSON format.

# Ingestion: Raw data is stored in Azure Data Lake Storage Gen2 in the Bronze Container as partitioned Parquet files to optimize cost.

# Orchestration: Microsoft Fabric Pipeline triggers the ingestion and manages the workflow.

# Transformation: Dataflow Gen2 cleans the data, loading it into Lakehouse.

# Screenshots:
Deployed lake storage and functionapp:
<img width="1661" height="674" alt="image" src="https://github.com/user-attachments/assets/ab86a30b-a19a-40bb-a05f-3c6ea97e8232" />

<img width="958" height="357" alt="image" src="https://github.com/user-attachments/assets/dcace2d4-41d4-4ca7-91ec-641c8ccd043c" />
<img width="1356" height="591" alt="image" src="https://github.com/user-attachments/assets/16276e8b-a810-40c8-bee2-4d6896345ba0" />

Transformation:

<img width="1841" height="865" alt="image" src="https://github.com/user-attachments/assets/d5add4dc-cbc4-4141-8f24-a1803f2a9c48" />
Silver(cleared data)
<img width="1686" height="546" alt="image" src="https://github.com/user-attachments/assets/573214c7-0693-4938-b032-389b711fa577" />


