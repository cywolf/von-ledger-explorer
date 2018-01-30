from oauth2client.service_account import ServiceAccountCredentials
import json
import time
from httplib2 import Http
import os

import requests
from apiclient import discovery

# TYPE_KEY_MAP = {
#    "1": ["dest", "identifier", "role", "type", "verkey"],
 #   "101": ["data", "identifier", "reqId", "signature", "txnTime"],
  #  "102": [
   #     "data",
   #    "identifier",
    #    "ref",
     #   "reqId",
      #  "signature",
       # "signature_type",
        # "txnTime"
   # ]
# }

HEADER_MAP= { 
    "1": ["Label", "Type", "Tags", "Description"],
    "102": ["Label", "Schema", "Claim Definition", "ref", "reqId"]
}

def update_sheets():
    # spreadsheetId = '13rFVDdfoJOLipB6upo46O9_QyDBWrhemexUo34LuX3A'
    spreadsheetId = os.environ['GOOGLE_SHEETS_ID']

    # Obtain access to google sheets api
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.abspath('./client_secret.json'), scopes)
    http_auth = credentials.authorize(Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build(
        'sheets', 'v4', http=http_auth, discoveryServiceUrl=discoveryUrl)

    # Write headers
    for record_type in HEADER_MAP:
        body = {'values': [
            HEADER_MAP[record_type]
        ]}

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheetId,
            range='Type%s!1:1' % (record_type),
            body=body,
            valueInputOption="RAW").execute()

    # Get ledger data from BCOVRIN
    ledger_response = requests.get('http://138.197.170.136/ledger/domain')
    counter_sheet_1 = 2
    counter_sheet_2 = 2
    #content = ledger_entry [2]
    for line in ledger_response.text.split('\n'):
        try:
            ledger_entry = json.loads(line)
        except json.decoder.JSONDecodeError:
            continue

       # sequence_number = ledger_entry[0]
        content = ledger_entry[1]

        # Get the type
        entity_type = content['type']

        # Handle each type differently
        if entity_type == "1":
            # This ledger item is an identity

            # For each of the attributes in this data type,
            # extract the value into a variable. If the attribute
            # isn't found in the data, use "" instead so that
            # program doesn't exit with an error

            Label = content['dest'] if 'dest' in content else ""
            Type = content['role'] if 'role' in content else ""
            Description = content['verkey'] if 'verkey' in content else ""
            Tags = content['identifier'] if 'identifier' in content else ""

            # We can transform the data as needed here. For example, if we wanted to
            # change the role number into a human readable role name we could do:

            # This should probably be at the top of the file if you use this.
            ROLE_MAP = {
                "0": "Trustee",
                "2": "Steward",
                "101": "Trust Anchor"
            }

            
            role_name = ROLE_MAP[Type] if Type in ROLE_MAP else "No Role"
           
            # We build a row in the spreadsheet. We can have as many columns as we want
            # for each row. Each entry in the array is a new column.

            # Here we can use our transformed data and create new rows as needed!
            row = [Label, role_name, Tags, Description]

            body = {'values': [row]}

            # Write ledger entries
            print('print sequence number_1 ' + str(counter_sheet_1))
            service.spreadsheets().values().update(
            spreadsheetId=spreadsheetId,
            range='Type%s!%s:%s' % (
                content['type'], counter_sheet_1, counter_sheet_1),
            body=body,
            valueInputOption="RAW").execute()
            counter_sheet_1 += 1 

        #elif entity_type == "101":

        #Label = content['identifier'] if 'identifier' in content else ""
        #Schema = content['data'] if 'data' in content else ""

        #row =[Label, Schema]  

        elif entity_type == "102": 
            
            ClaimDef = content['signature'] if 'signature' in content else "" 
            Ref = content['ref'] if 'ref' in content else ""
            reqId = content['reqId'] if 'reqId' in content else ""
                    
            for line in ledger_response.text.split('\n'):
                try:
                    ledger_entry = json.loads(line)
                except json.decoder.JSONDecodeError:
                    continue

                related_sequence_number = ledger_entry[0]

                if related_sequence_number == Ref:
                    related_content = ledger_entry[1]

                    Label = related_content['identifier'] if 'identifier' in related_content else ""
                    Schema = related_content['data'] if 'data' in related_content else ""
                    
            row = [str(Label), str(Schema), str(ClaimDef), str(Ref), str(reqId)]
            body = {'values': [row]}
            
            # Write ledger entries
            print('print sequence number_2 ' + str(counter_sheet_2))
            service.spreadsheets().values().update(
             spreadsheetId=spreadsheetId,
            range='Type%s!%s:%s' % (
                content['type'], counter_sheet_2, counter_sheet_2),
            body=body,
            valueInputOption="RAW").execute()

            counter_sheet_2 += 1 

            #legal_name = ...
            #address = ...
            #combined = 'Legal name: ' + legal_name + ' Address: ' + address
            #example = legal_name + ' || ' + address
            # We build the expected request format using the row above
       

        # Avoid rate limiting
        time.sleep(0.2)

    #claim_response = requests.get('https://django-devex-von-dev.pathfinder.gov.bc.ca/api/v1/verifiableclaims')
    #claims = claim_response.json()
    #for claim in claims:
    ###
        
        # do stuff
        #pass


def main():
    while(True):
        update_sheets()
        time.sleep(60)


if __name__ == '__main__':
    main()