# BCOVRIN to Google Sheets Connector

## Install Instructions

1. Install `pipenv` from https://github.com/pypa/pipenv

2. Run `pipenv install requests google-api-python-client`

3. Use this link [https://console.developers.google.com/start/api?id=sheets.googleapis.com] to enable Google Sheets API access and create a new service account key in JSON format. Rename the file 'client_secret.json' and add it to this directory.

4. Create a new google spreadsheet and find its id which is in the url. If `https://docs.google.com/spreadsheets/d/1Uyj6-THbswus2DqYH2kRtlcyiLzL1sjbz9itez6qWAY/edit#gid=0` is the url, then `1Uyj6-THbswus2DqYH2kRtlcyiLzL1sjbz9itez6qWAY` is the id.

5. The Google sheet's access permissions **must** be set to *public can edit*. You can find these settings under share>advanced.

6. The spreadsheet must have at least 3 worksheets: Type1, Type101, and Type102.


## Running

Use the id above in the following command:


```python
# Make sure you replace this id with your new id
GOOGLE_SHEETS_ID=1Uyj6-THbswus2DqYH2kRtlcyiLzL1sjbz9itez6qWAY pipenv run python main.py
```
