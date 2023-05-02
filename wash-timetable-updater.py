from __future__ import print_function

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

import os.path
from datetime import datetime
from datetime import timedelta

LOCATION = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTALS = service_account.Credentials.from_service_account_file(
     LOCATION+'credentials.json', scopes=SCOPES)
# ID for production 
# SPREADSHEET_ID = "1f4aUWR46jZeRy_sla25cyCBAnGf0xZ68gOiUmJ3Ekuo"
# ID for testing
SPREADSHEET_ID = '14rNlHqmBvhNh8Codp8P059KVk8Ih3CypsmiEdGQBsNg'
RANGE_PREFIX = 'Aktualno!'
# [[RANGE_FROM, RANGE_TO]]
RANGES = [["C25:I33", "C13:I21"],
          ["L25:R33", "L13:R21"]
          ]

def update_values(service, spreadsheet_id, range_name, value_input_option,
                  values):
    
    try:
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=RANGE_PREFIX+range_name,
            valueInputOption=value_input_option, body=body).execute()
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def main():       
    try: 
        service = build('sheets', 'v4', credentials=CREDENTALS)
        sheet = service.spreadsheets()

        empty = [["" for i in range(7)] for i in range(9)]
        for RANGE in RANGES:
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                            range=RANGE_PREFIX+RANGE[0]).execute()
                values = result.get('values', [])
                update_values(service, SPREADSHEET_ID, RANGE[1], "USER_ENTERED", empty)
                update_values(service, SPREADSHEET_ID, RANGE[1], "USER_ENTERED", values)
                update_values(service, SPREADSHEET_ID, RANGE[0], "USER_ENTERED", empty)
        
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_PREFIX+"B24").execute()
        value = result.get('values',[])[0][0]
        update_values(service, SPREADSHEET_ID, "B12", "USER_ENTERED", [[value]])
        
        day = int(value[8:10])
        month = int(value[11:13])
        Date_from = datetime(datetime.today().year, month, day) + timedelta(days=1)
        Date_to = Date_from + timedelta(days=6)

        value = "{:02}.{:02} - {:02}.{:02}".format(Date_from.day, Date_from.month, Date_to.day, Date_to.month)
        update_values(service,SPREADSHEET_ID, "B24", "USER_ENTERED", [[value]])
    except HttpError as err:
        print(err)
    

if __name__ == '__main__':
    main()
