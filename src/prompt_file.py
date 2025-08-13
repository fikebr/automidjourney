import re
import sqlite3
import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
import config
import logging

def save_usage(prompts):
    
    style_ids = []
    prompt_ids = []
    subject_ids = []
    
    for prompt in prompts:
        subject_id = None
        style_id = None
        prompt_id = None
        
        # Check for subject/style pattern
        subject_style_match = re.search(r' u(\d+)-y(\d+)$', prompt)
        if subject_style_match:
            (subject_id, style_id) = subject_style_match.groups()
            subject_id = int(subject_id)
            style_id = int(style_id)
            subject_ids.append(subject_id)
            style_ids.append(style_id)
        
        # Check for prompt_id pattern
        prompt_match = re.search(r' p(\d+)$', prompt)
        if prompt_match:
            prompt_id = int(prompt_match.group(1))
            prompt_ids.append(prompt_id)
    
    db = sqlite3.connect(config.DB_NAME)
    cursor = db.cursor()

    table_name = "usage"
    columns = "item_id, table_name, timestamp"
    placeholders = "?, ?, ?"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data_subjects = [(subject_id, 'subjects', timestamp,) for subject_id in subject_ids]
    data_styles = [(style_id, 'styles', timestamp,) for style_id in style_ids]
    data_prompts = [(prompt_id, 'prompts', timestamp,) for prompt_id in prompt_ids]

    data = data_subjects + data_styles + data_prompts
    # pprint.pprint(data)

    try:
        for entry in data:
            # pprint.pprint(entry)
            cursor.execute(
                f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                entry,
            )
            db.commit()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while inserting data into {table_name}: {e}")


def get_random_prompts():
    """Query the prompt_tmp table for random prompts."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        
        # Query for random prompts from prompts_tmp table
        cursor.execute(
            "SELECT prompts FROM prompts_tmp ORDER BY RANDOM()",
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

def write_prompts_to_file(prompts, filename, count=100):
    """Write prompts to the specified file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            prompts_written = 0
            prompt_index = 0
            
            while prompts_written < count:
                if prompt_index >= len(prompts):
                    # If we've used all prompts, start over from the beginning
                    prompt_index = 0
                
                f.write(f"{prompts[prompt_index]}\n")
                prompts_written += 1
                prompt_index += 1
        
        logging.info(f"Successfully wrote {prompts_written} prompts to {filename}")
        return True
        
    except IOError as e:
        logging.error(f"Error writing to file {filename}: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error writing to file: {e}")
        return False

def run(count=100):
    """Main function to get random prompts and write them to file."""
    logging.info("==== START PROMPT FILE GENERATION ====")
    
    # Get random prompts
    prompts = get_random_prompts()
    
    if not prompts:
        logging.error("No prompts retrieved from database")
        return
    
    # Write prompts to file
    filename = config.PROMPT_FILE_NAME
    success = write_prompts_to_file(prompts, filename, count)
    
    if success:
        save_usage(prompts)
        logging.info(f"Prompt file generation completed successfully: {filename}")
    else:
        logging.error("Failed to write prompts to file")
    
    logging.info("==== COMPLETE PROMPT FILE GENERATION ====")

def main():
    run()

if __name__ == "__main__":
    main() 