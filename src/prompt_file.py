import sqlite3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
import config
import logging

def get_random_prompts(limit=100):
    """Query the prompt_tmp table for random prompts."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        
        # Query for random prompts from prompts_tmp table
        cursor.execute(
            "SELECT prompts FROM prompts_tmp ORDER BY RANDOM() LIMIT ?",
            (limit,)
        )
        
        prompts = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        logging.info(f"Retrieved {len(prompts)} random prompts from prompts_tmp table")
        return prompts
        
    except sqlite3.Error as e:
        logging.error(f"Database error while retrieving prompts: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error while retrieving prompts: {e}")
        return []

def write_prompts_to_file(prompts, filename):
    """Write prompts to the specified file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for prompt in prompts:
                f.write(f"{prompt}\n")
        
        logging.info(f"Successfully wrote {len(prompts)} prompts to {filename}")
        return True
        
    except IOError as e:
        logging.error(f"Error writing to file {filename}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error writing to file: {e}")
        return False

def run():
    """Main function to get random prompts and write them to file."""
    logging.info("==== START PROMPT FILE GENERATION ====")
    
    # Get random prompts
    prompts = get_random_prompts(100)
    
    if not prompts:
        logging.error("No prompts retrieved from database")
        return
    
    # Write prompts to file
    filename = config.PROMPT_FILE_NAME
    success = write_prompts_to_file(prompts, filename)
    
    if success:
        logging.info(f"Prompt file generation completed successfully: {filename}")
    else:
        logging.error("Failed to write prompts to file")
    
    logging.info("==== COMPLETE PROMPT FILE GENERATION ====")

def main():
    run()

if __name__ == "__main__":
    main() 