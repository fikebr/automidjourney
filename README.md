# Automate Midjourney

A system to automate running prompts on Midjourney using a SQLite database and Google Sheets integration. The system manages subjects, styles, and prompts, tracking their usage to ensure even distribution.

## Features

- Database-driven prompt generation combining subjects and styles
- Google Sheets integration for easy data management
- Usage tracking to ensure even distribution of prompts
- Wildcard system for dynamic prompt elements
- Automated prompt submission to Midjourney
- Configurable delays between prompts
- Comprehensive logging system
- Rating-based prompt selection

## Components

- `auto_midjourney.py`: Main orchestration script
- `get_prompts.py`: Generates prompts from database components
- `update_db.py`: Syncs Google Sheets data to SQLite
- `automate.py`: Handles the automation of prompt submission
- `config.py`: Central configuration management
- `log.py`: Logging configuration and management

## Setup

1. Create a Google Cloud project and enable the Sheets API
2. Download service account credentials as `key.json`
3. Set up your Google Sheet with the following tabs:
   - subjects
   - styles
   - prompts
   - wildcards
   - control
   - usage
4. Configure `config.py` with your settings
5. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main automation script:
   ```bash
   python auto_midjourney.py
   ```

2. Or run individual components:
   ```bash
   python update_db.py    # Sync from Google Sheets
   python get_prompts.py  # Generate prompts
   python automate.py     # Run automation
   ```

## Configuration

Key settings in `config.py`:
- `DB_NAME`: SQLite database file name
- `prompt_prefix`: Optional prefix for all prompts
- `prompt_suffix`: Optional suffix for all prompts
- `automate_sleep`: Base delay between prompts
- `promptbar_image`: Screenshot for identifying Midjourney input
- `save_prompts_to_txt`: Option to save prompts to text file

## Future Enhancements

1. Web interface for database management
2. Support for additional AI image generators (Dall-E, Flux)
3. Tag-based prompt selection
4. Advanced scheduling features
5. Mouse movement during long sleeps to prevent screensaver
6. Prompt analytics and optimization
7. Multi-user support
8. API integration options
9. Custom prompt templates
10. Batch processing capabilities
11. implement a "big sleep" feature so that I can run this script like a service. the "big sleep" could also be a "start time" instead of a number of seconds.
12. implement a system for suffix and prefix in the google sheet
13. add a bigger sleep after every X prompts. (that )
14. is there a world where i can monetize this system?
15. record subject\style\prompt usage so that i can pick prompts based on lessed used. this would require writing to the sheets not just reading the sheets.
16. switch from sheets to a true online DB and a website to manage the DB
17. pick prompts based on tag query

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Todo

[Add your chosen license here]