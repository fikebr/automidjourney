import argparse
from src import update_db
from src import get_prompts
from src import automate
from src import prompt_file
from src.log import setup_logging

setup_logging()


def main():
    update_db.run()
    get_prompts.run()
    automate.run()


def cli():
    parser = argparse.ArgumentParser(
        description="Auto Midjourney CLI - A comprehensive tool for automating Midjourney image generation workflows",
        epilog="This tool provides various commands to manage prompts, update databases, and automate Midjourney processes."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Update database command
    update_parser = subparsers.add_parser(
        "update_db", 
        help="Update SQLite database from Google Sheets"
    )
    update_parser.description = "Fetches data from Google Sheets and updates the local SQLite database with the latest information."
    
    # Get prompts command
    prompts_parser = subparsers.add_parser(
        "get_prompts", 
        help="Retrieve prompts from the database"
    )
    prompts_parser.description = "Retrieves and processes prompts from the local database for use in automation."
    
    # Automate command
    automate_parser = subparsers.add_parser(
        "automate", 
        help="Run the Midjourney automation"
    )
    automate_parser.description = "Executes the main automation workflow for Midjourney image generation."
    
    # Prompt file command
    prompt_file_parser = subparsers.add_parser(
        "prompt_file", 
        help="Generate a file with random prompts"
    )
    prompt_file_parser.description = "Queries the prompt_tmp table for 100 random prompts and writes them to a file."

    # All command
    all_parser = subparsers.add_parser(
        "all", 
        help="Run all commands in sequence"
    )
    all_parser.description = "Executes update_db, get_prompts, and automate in sequence (original behavior)."
    
    
    args = parser.parse_args()
    
    if args.command == "update_db":
        update_db.run()
    elif args.command == "get_prompts":
        get_prompts.run()
    elif args.command == "automate":
        automate.run()
    elif args.command == "all":
        main()
    elif args.command == "prompt_file":
        prompt_file.run()
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
