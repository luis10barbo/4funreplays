from lib import google
from lib.google import QUEUE_OUTPUT

class GoogleSpreadsheetHandler():
    spreadsheet_id = ""
    
    def get_spreadsheet_id_from_config(self, config_json:dict[str,dict]):
        self.spreadsheet_id = config_json["Google"]["SpreadsheetId"]
    
    def get_queue_from_google(self, spreadsheet_id = ""):
        if spreadsheet_id == "":
            spreadsheet_id = self.spreadsheet_id
        
        google_api = google.api()
        
        google_api.set_spreadsheet(spreadsheet_id=f"{spreadsheet_id}")
        return google_api.create_spreadsheet()
        