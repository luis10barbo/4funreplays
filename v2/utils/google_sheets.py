from constants.paths import PATH_SHEET
from model.sheet_obr import ColumnSheetObr
from utils.logger import debug
def parse_sheets_string():
    with open(PATH_SHEET, "r") as file:
        debug(f"Found sheet at {PATH_SHEET}")
        sheets_data = file.read()
        lines = sheets_data.split("\n")

        if len(lines) < 1:
            return None
        parsed_columns: list[list[str]] = []
        for line in lines:
            columns = line.split("	")
            parsed_columns.append(columns)

        return parsed_columns
    
def parse_sheets_obr():
    parsed_columns = parse_sheets_string()
    if parsed_columns is None or len(parsed_columns) < 2:
        return None
    
    columnsObr: list[ColumnSheetObr] = []
    debug("Parsing sheet using OBR standard")
    for i, column in enumerate(parsed_columns):
        if i == 0:
            continue
        columnObr: ColumnSheetObr = {
            "perfil": column[0],
            "mapa": column[1],
            "skin": column[2],
            "skin_local": column[3],
            "replay": column[4],
            "done": True if column[5] == "TRUE" else False,
            "posted": True if column[6] == "TRUE" else False 
        }
        columnsObr.append(columnObr)
    
    debug(f"Parsed {len(columnsObr) - 1} columns")
    return columnsObr
        
