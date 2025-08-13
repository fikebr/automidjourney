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
        epilog="\n\n"
    )
    
    # Add command flags for multiple command execution
    parser.add_argument(
        "--update_db", 
        action="store_true",
        help="Update SQLite database from Google Sheets"
    )
    parser.add_argument(
        "--get_prompts", 
        action="store_true",
        help="Retrieve prompts from the database"
    )
    parser.add_argument(
        "--automate", 
        action="store_true",
        help="Run the Midjourney automation"
    )
    parser.add_argument(
        "--prompt_file", 
        action="store_true",
        help="Generate a file with random prompts"
    )
    parser.add_argument(
        "--count", 
        type=int,
        default=100,
        help="Number of prompts to write to file (default: 100)"
    )
    
    args = parser.parse_args()
    
    # Check if any flags are provided
    flags_provided = any([args.update_db, args.get_prompts, args.automate, args.prompt_file])
    
    if flags_provided:
        # Execute commands based on flags
        if args.update_db:
            print("Running: update_db")
            update_db.run()
        if args.get_prompts:
            print("Running: get_prompts")
            get_prompts.run()
        if args.automate:
            print("Running: automate")
            automate.run()
        if args.prompt_file:
            print("Running: prompt_file")
            prompt_file.run(args.count)
    else:
        # No flags provided, show help
        parser.print_help()


if __name__ == "__main__":
    cli()
