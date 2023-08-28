# How to

Prerequisites:

1) Install gcloud
   Use instructions here - https://cloud.google.com/sdk/docs/install

2) Install script dependencies using pip
   $ pip install google-auth google-auth-httplib2 google-api-python-client google-cloud-iam
   $ pip install pandas firebase-admin

Authentication:
3) Authenticate to Google Cloud
   $ gcloud auth application-default login

4) Find projects list from Google Cloud account
   $ gcloud projects list

Execution:
5 Run Python script
   $ python3 iam.py --project_id <project_id>

   This execution of script generate combined_data_<date>.xls in the current working directory.
