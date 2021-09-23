from googleapiclient.discovery import build
import datetime
from httplib2 import Http
from oauth2client import file, client, tools
from typing import List, Any
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


class Spreadsheet:

    def __init__(self, spreadsheet_id: str, token_file: str, credentials_file: str):
        """
        A constructor for this spreadsheet, opening it and ensuring user is authorized.
        """
        self.spreadsheet_id = spreadsheet_id
        store = file.Storage(token_file)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credentials_file, SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('sheets', 'v4', http=creds.authorize(Http()))

    def read_value(
        self,
        page: str,
        column: str,
        row: str
    ) -> str:
        """
        Reads the current value of the specified page, at the specified row and column
        """
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id, range=(page + "!" + column + row)).execute()
        result = result.get('values', [])
        return result[0][0]

    def write_value(
        self,
        page: str,
        column: str,
        row: str,
        value: Any
    ) -> None:
        """
        Writes data the specified column/row from the specified page from this spreadsheet.
        """
        dest = page + "!" + column + row
        values = [[value]]
        body = {'values': values}
        result = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,
                                                             range=dest,
                                                             valueInputOption="USER_ENTERED",
                                                             body=body
                                                             ).execute()

    def find_empty_cell_in_column(
        self,
        page: str,
        column: str,
        row: str
    ) -> int:
        """
        Finds the first empty row in the specified column.
        """
        search = page + "!" + column + row + ":" + column
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id, range=search).execute()
        current_row = 0
        result = result.get('values', [])
        current_row += int(row) + len(result)
        return current_row

    def write_row(
            self,
            page: str,
            column_start: str,
            column_end: str,
            row: str,
            data: List[Any]
    ) -> None:
        """
        Writes the values in data, on the designated page, in the specified row,
        from column start to column end
        """
        location = page + "!" + column_start + row + ":" + column_end + row
        values = [data]
        body = {'values': values}
        self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,
                                                    range=location,
                                                    valueInputOption="USER_ENTERED",
                                                    body=body).execute()

    def write_column(
            self,
            page: str,
            column: str,
            row_start: str,
            row_end: str,
            data: List[Any]
    ) -> None:
        """
        Writes the values in data, on the designated page, in the specified row,
        from column start to column end
        """
        location = page + "!" + column + row_start + ":" + column + row_end
        values = [[d] for d in data]
        body = {'values': values}
        self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,
                                                    range=location,
                                                    valueInputOption="USER_ENTERED",
                                                    body=body).execute()

    def read_block(
        self,
        page: str,
        column_start: str,
        column_end: str,
        row_start: str,
        row_end: str
    ) -> List[List[str]]:
        """
        Reads a Rectangular block of data in the specified sheet.
        """
        location = page + "!" + column_start + row_start + ":" + column_end + row_end
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id, range=location).execute()
        result = result.get('values', [])
        return result

    def write_block(
        self,
        page: str,
        column_start: str,
        column_end: str,
        row_start: str,
        row_end: str,
        data: List[List[str]]
    ) -> None:
        """
        Writes a rectangular block of data in the designated sheet
        """
        location = page + "!" + column_start + row_start + ":" + column_end + row_end
        body = {'values': data}
        self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,
                                                    range=location,
                                                    valueInputOption="USER_ENTERED",
                                                    body=body).execute()

    def read_column(
        self,
        page: str,
        column: str,
        row_start: str,
        row_end: str
    ) -> List[str]:
        """
        Reads the specified column of data of the specified page, from the start and ending rows
        """
        location = page + "!" + column + row_start + ":" + column + row_end
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id, range=location).execute()
        result = result.get('values', [])
        values = []

        for value in result:
            values.append(value[0])
        return values
