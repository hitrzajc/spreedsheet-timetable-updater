from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import datetime
from datetime import timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '14rNlHqmBvhNh8Codp8P059KVk8Ih3CypsmiEdGQBsNg'
RANGE_PREFIX = 'Sheet1!'

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
        # print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try: 
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        for RANGE in RANGES:
                result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                            range=RANGE_PREFIX+RANGE[0]).execute()
                values = result.get('values', [])
                empty = [["" for i in range(7)] for i in range(9)]
                update_values(service, SPREADSHEET_ID, RANGE[1],"USER_ENTERED", empty)
                update_values(service, SPREADSHEET_ID, RANGE[1],"USER_ENTERED", values)
                update_values(service, SPREADSHEET_ID, RANGE[0],"USER_ENTERED", empty)
        
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_PREFIX+"B24").execute()
        value = result.get('values',[])[0][0]
        update_values(service, SPREADSHEET_ID, "B12", "USER_ENTERED", [[value]])
        
        day = int(value[7:9])
        month = int(value[10:12])
        Date_from = datetime(datetime.today().year, month, day) + timedelta(days=1)
        Date_to = Date_from + timedelta(days=6)

        value = "{:02}.{:02}.-{:02}.{:02}.".format(Date_from.day, Date_from.month, Date_to.day, Date_to.month)
        update_values(service,SPREADSHEET_ID, "B24", "USER_ENTERED", [[value]])
        print("")

    except HttpError as err:
        print(err)
    

if __name__ == '__main__':
    main()