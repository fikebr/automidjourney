# Automate Midjourney

A comprehensive CLI tool for automating Midjourney image generation workflows using a SQLite database and Google Sheets integration. The system manages subjects, styles, and prompts, tracking their usage to ensure even distribution.

## Features

- **CLI Interface**: Command-line interface with multiple commands for different operations
- **Database-driven prompt generation**: Combines subjects and styles with unique identifiers
- **Google Sheets integration**: Easy data management and synchronization
- **Usage tracking**: Ensures even distribution of prompts, subjects, and styles
- **Wildcard system**: Dynamic prompt elements for variety
- **Automated prompt submission**: Direct integration with Midjourney
- **Configurable delays**: Between prompts and automation cycles
- **Comprehensive logging**: File and console logging with detailed tracking
- **Rating-based selection**: Intelligent prompt selection based on ratings
- **Random prompt file generation**: Export random prompts for external use

## Project Structure

```
automidjourney/
├── auto_midjourney.py          # Main CLI entry point
├── src/                        # Core application modules
│   ├── __init__.py
│   ├── automate.py             # Midjourney automation logic
│   ├── get_prompts.py          # Prompt generation and database operations
│   ├── log.py                  # Logging configuration
│   ├── prompt_file.py          # Random prompt file generation
│   └── update_db.py            # Google Sheets to SQLite synchronization
├── config/                     # Configuration and assets
│   ├── config.py               # Application configuration
│   ├── key.json                # Google Sheets API credentials
│   ├── promptbar.png           # UI element reference image
│   └── queued.png              # UI element reference image
├── logs/                       # Application logs
├── automidjourney.db           # SQLite database
├── pyproject.toml              # Project dependencies (uv)
└── README.md                   # This file
```

## Setup

1. **Google Cloud Setup**:
   - Create a Google Cloud project and enable the Sheets API
   - Download service account credentials as `config/key.json`

2. **Google Sheets Structure**:
   Set up your Google Sheet with the following tabs:
   - `subjects`: Subject data with ratings and status
   - `styles`: Style data with ratings and status  
   - `prompts`: Prompt data with ratings and status
   - `wildcards`: Dynamic replacement values
   - `control`: Configuration for prompt counts by rating
   - `usage`: Usage tracking (auto-populated)

3. **Install Dependencies**:
   ```bash
   uv sync
   ```

4. **Configure Settings**:
   Edit `config/config.py` with your specific settings:
   - `SPREADSHEET_ID`: Your Google Sheet ID
   - `PROMPT_FILE_NAME`: Output file for random prompts
   - `prompt_prefix`/`prompt_suffix`: Global prompt modifiers
   - `automate_sleep`: Delay between automation actions

## CLI Usage

The application provides a comprehensive CLI with the following commands:

### Main Commands

```bash
# Update database from Google Sheets
uv run python auto_midjourney.py update_db

# Generate prompts from database components
uv run python auto_midjourney.py get_prompts

# Run Midjourney automation
uv run python auto_midjourney.py automate

# Generate random prompt file
uv run python auto_midjourney.py prompt_file

# Run all commands in sequence (original behavior)
uv run python auto_midjourney.py all

# Show help
uv run python auto_midjourney.py -h
```

### Command Descriptions

- **`update_db`**: Fetches data from Google Sheets and updates the local SQLite database
- **`get_prompts`**: Retrieves and processes prompts from the local database for use in automation
- **`automate`**: Executes the main automation workflow for Midjourney image generation
- **`prompt_file`**: Queries the prompts_tmp table for 100 random prompts and writes them to a file
- **`all`**: Executes update_db, get_prompts, and automate in sequence

### Help for Specific Commands

```bash
# Get detailed help for any command
uv run python auto_midjourney.py update_db -h
uv run python auto_midjourney.py get_prompts -h
uv run python auto_midjourney.py automate -h
uv run python auto_midjourney.py prompt_file -h
```

## Configuration

### Key Settings in `config/config.py`

- **`SPREADSHEET_ID`**: Google Sheets document ID
- **`DB_NAME`**: SQLite database file name
- **`PROMPT_FILE_NAME`**: Output file path for random prompts
- **`prompt_prefix`**: Optional prefix for all generated prompts
- **`prompt_suffix`**: Optional suffix for all generated prompts
- **`automate_sleep`**: Base delay between automation actions
- **`promptbar_image`**: Path to UI reference image
- **`save_prompts_to_txt`**: Option to save prompts to text file

### Database Schema

The system uses several tables:
- **`subjects`**: Available subjects with ratings and usage tracking
- **`styles`**: Available styles with ratings and usage tracking
- **`prompts`**: Pre-defined prompts with ratings and usage tracking
- **`wildcards`**: Dynamic replacement values for prompt templates
- **`control`**: Configuration for how many items to select by rating
- **`usage`**: Tracks when items are used (auto-populated)
- **`prompts_tmp`**: Temporary storage for generated prompts

## Features in Detail

### Prompt Generation
- Combines subjects and styles with unique identifiers (e.g., `u123-y456`)
- Adds prompt IDs to existing prompts (e.g., `p789`)
- Supports wildcard replacement (e.g., `__color__` → `red`)
- Configurable prefix/suffix for all prompts

### Usage Tracking
- Records when subjects, styles, and prompts are used
- Enables intelligent selection based on usage patterns
- Prevents overuse of specific items

### Automation
- Automated interaction with Midjourney interface
- Configurable delays between actions
- Screenshot-based UI element detection
- Error handling and recovery

## Future Enhancements

1. **Web Interface**: Database management through web UI
2. **Multi-Platform Support**: Additional AI image generators (Dall-E, Flux)
3. **Advanced Scheduling**: Time-based automation with start/stop times
4. **Tag-Based Selection**: Query prompts by tags and categories
5. **Analytics Dashboard**: Usage statistics and optimization insights
6. **API Integration**: REST API for external integrations
7. **Custom Templates**: Advanced prompt template system
8. **Batch Processing**: Handle multiple prompts simultaneously
9. **Monetization Features**: Potential for commercial use
10. **Cloud Database**: Migration from Google Sheets to dedicated database
11. **Big Sleep Feature**: Service-like operation with configurable sleep cycles
12. **Dynamic Prefix/Suffix**: Sheet-based prefix/suffix management
13. **Usage-Based Selection**: Prioritize less-used items automatically

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]