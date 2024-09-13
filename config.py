# config.py

# Google Sheets configuration
SPREADSHEET_ID = "1sC9liaNriZvt5zeDKGsNEPOizM4AD89phO79GphWsqE"

# Database configuration
DB_NAME = "automidjourney.db"

# Google Sheets API configuration
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"
KEY_FILE = "key.json"

# Table configurations
TABLE_CONFIGS = {
    "subjects": {
        "sheet_name": "subjects",
        "table_name": "subjects",
        "columns": ["subject_id", "subject", "status", "tags", "date", "rating"],
        "int_columns": ["subject_id", "rating"],
    },
    "styles": {
        "sheet_name": "styles",
        "table_name": "styles",
        "columns": ["style_id", "style", "status", "tags", "date", "rating"],
        "int_columns": ["style_id", "rating"],
    },
    "prompts": {
        "sheet_name": "prompts",
        "table_name": "prompts",
        "columns": ["prompt_id", "prompt", "status", "tags", "date", "rating"],
        "int_columns": ["prompt_id", "rating"],
    },
    "wildcards": {
        "sheet_name": "wildcards",
        "table_name": "wildcards",
        "columns": ["wildcard", "value"],
        "int_columns": [],
    },
    "control": {
        "sheet_name": "control",
        "table_name": "control",
        "columns": ["tablename", "rating", "count"],
        "int_columns": ["rating", "count"],
    },
}

prompt_prefix = ""
prompt_suffix = ""

promptbar_image = "promptbar.png"
automate_sleep = 50

save_prompts_to_txt = False
