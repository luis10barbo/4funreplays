# from __future__ import print_function
import os
from googleapiclient.discovery import build

import json
from google.oauth2 import service_account

from lib import logger

MAIN_FOLDER = os.getcwd()
AUTHORIZATION_FILE = os.path.join(MAIN_FOLDER, 'secrets', 'google', 'authorization.json')
QUEUE_OUTPUT = os.path.join(MAIN_FOLDER, 'info', 'queue.json')

class api():
    SERVICE_ACCOUNT_FILE = f"{AUTHORIZATION_FILE}"
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # If modifying these scopes, delete the file token.json.


    # The ID sample spreadsheet.
    # SAMPLE_SPREADSHEET_ID = '1TYTDllTN4xrcAa3T31rU5T2Eo5vujLZcZ5qJdyu5zrQ'
    
    service = build('sheets', 'v4', credentials=creds)

    def set_spreadsheet(self, spreadsheet_id):
        logger.info(f"Spreadsheet id set to {spreadsheet_id}")
        self.sample_spreadsheet_id = spreadsheet_id

    # Call the Sheets API
    def request(self):
        sheet = self.service.spreadsheets()
        result = (sheet.values().get(spreadsheetId=self.sample_spreadsheet_id,
                                    range='B2:G').execute())['values']

        dictres = result.copy()
        for x in dictres:
            x[0] = str(x[0]).replace("'", "")
            x[3] = str(x[3]).replace("'", "")
            
        #print (dictres)
        return dictres
        
    def create_spreadsheet(self):
        logger.info("Requesting google spreadsheet")
        result = self.request()
        queue = []
        queue_template = {'profile' : '', 'map' : '' , 'skin' : '' , "replay" : "",  'replay_id' : '', "replay_link" : ""}

        # create queue
        for i, queue_entry in enumerate(result):
            if queue_entry == []:
                pass
            queue.append(queue_template.copy())
            queue[i]["profile"] = queue_entry[1]
            queue[i]["map"] = queue_entry[2]
            queue[i]["skin"] = queue_entry[3]
            queue[i]['replay_id'] = i+1
            queue[i]["replay_link"] = queue_entry[4]
            queue[i]["cursor_size"] = float(queue_entry[5])
            queue = queue.copy()

        with open(f'{QUEUE_OUTPUT}', 'w') as file:
            json.dump(queue, file, sort_keys=True, indent=4)
            
        logger.info("Request for google spreadsheet has been sucessful")

        return queue
    
        
    



    
