from google.oauth2 import service_account
from googleapiclient.discovery import build
import sqlite3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
import config
import logging

def convert_types(row, table_config):
    try:
        converted_row = list(row)
        for i, col in enumerate(table_config["columns"]):
            if col in table_config["int_columns"]:
                converted_row[i] = int(row[i]) if row[i] else None
        return tuple(converted_row)
    except ValueError as e:
        logging.error(f"Error converting types for row {row}: {e}")
        return None


def update_sqlite_table(data, table_config):
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    table_name = table_config["table_name"]
    columns = ", ".join(table_config["columns"])

    # Delete existing data
    try:
        cursor.execute(f"DELETE FROM {table_name}")
    except sqlite3.Error as e:
        logging.error(f"Error clearing existing data from {table_name}: {e}")
        conn.close()
        return

    # Insert new data
    skipped_records = 0
    placeholders = ", ".join(["?" for _ in table_config["columns"]])
    for row in data:
        converted_row = convert_types(row, table_config)
        if converted_row is None:
            skipped_records += 1
            continue

        try:
            cursor.execute(
                f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                converted_row,
            )
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                logging.info(
                    f"DUPE : {table_name} : {converted_row[0]} | {converted_row[1]}"
                )
                skipped_records += 1
            else:
                logging.warn(f"Integrity error occurred in {table_name}: {e}")
        except sqlite3.Error as e:
            logging.error(
                f"An error occurred while inserting data into {table_name}: {e}"
            )
            skipped_records += 1

    conn.commit()
    conn.close()

    logging.info(
        f"Table {table_name} update completed. {skipped_records} records skipped."
    )


def get_google_sheet_data(sheet_name):
    try:
        credentials = service_account.Credentials.from_service_account_file(config.KEY_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=config.SPREADSHEET_ID, range=sheet_name)
            .execute()
        )
        return result.get("values", [])
    except Exception as e:
        logging.error(f"get_google_sheet_data : {sheet_name} : {e}")
        return None


def run():
    logging.info("==== START ====")
    for table, table_config in config.TABLE_CONFIGS.items():
        logging.info(f"TABLE :: {table}...")
        data = get_google_sheet_data(table_config["sheet_name"])
        if data:
            # Skip the first row (column names)
            data = data[1:]
            if not data:
                logging.warn(
                    f"No data found after skipping the header row for {table}."
                )
                continue
            update_sqlite_table(data, table_config)
            logging.info(f"{table} table updated successfully.")
        else:
            logging.warn(f"Failed to retrieve data from Google Sheets for {table}.")
    logging.info("==== COMPLETE ====")


def main():
    run()


if __name__ == "__main__":
    main()
