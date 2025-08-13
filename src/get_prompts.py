import sqlite3
import datetime
import pprint
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
import config
import re
import logging

# TODO: make this a config option
usage_to_query = 0
usage_amount_to_get = 10


def combine_subjects(subjects, styles, subject_ids, style_ids):
    """Combines subjects and styles to create prompts."""
    prompts = []
    for i, subject in enumerate(subjects):
        for j, style in enumerate(styles):
            prompt = f"{subject} | in the style of {style} u{subject_ids[i]}-y{style_ids[j]}"
            prompts.append(prompt)
    return prompts


def get_styles(db, control):
    """Retrieves styles from the database based on control."""
    styles = []
    style_ids = []
    name = "style"
    
    # Get styles based on rating from the database
    for rating, count in control["styles"].items():
        # sql = f"SELECT style_id, style FROM styles WHERE rating = {rating} AND status = 'open' ORDER BY RANDOM() LIMIT {count};"
        sql = f"select {name}_id, {name} from {name}_usage where rating = {rating} limit {count};"
        # sql = f"SELECT p.{name}_id, p.{name}, COUNT(u.item_id) AS usage_count FROM {name}s p LEFT JOIN usage u ON p.{name}_id = u.item_id WHERE p.status = 'open' and p.rating = {rating} and u.table_name = '{name}s' GROUP BY p.{name} ORDER BY usage_count ASC, RANDOM() LIMIT {count};"
        rows = db.execute(sql).fetchall()
        styles.extend([row[1] for row in rows])
        style_ids.extend([row[0] for row in rows])
        
    # Get styles based on usage_to_query
    sql = f"select {name}_id, {name} from {name}_usage where usage_count = {usage_to_query} order by usage_count desc limit {usage_amount_to_get};"
    rows = db.execute(sql).fetchall()
    styles.extend([row[1] for row in rows])
    style_ids.extend([row[0] for row in rows])
    
    return styles, style_ids


def get_prompts(db, control):
    """Retrieves prompts from the database based on control."""
    prompts = []
    prompt_ids = []
    name = "prompt"
    
    # Get prompts based on rating from the database
    for rating, count in control["prompts"].items():
        # sql = f"SELECT prompt_id, prompt FROM prompts WHERE rating = {rating} AND status = 'open' ORDER BY RANDOM() LIMIT {count};"
        sql = f"select {name}_id, {name} from {name}_usage where rating = {rating} limit {count};"
        # sql = f"SELECT p.{name}_id, p.{name}, COUNT(u.item_id) AS usage_count FROM {name}s p LEFT JOIN usage u ON p.{name}_id = u.item_id WHERE p.status = 'open' and p.rating = {rating} and u.table_name = '{name}s' GROUP BY p.{name} ORDER BY usage_count ASC, RANDOM() LIMIT {count};"
        rows = db.execute(sql).fetchall()
        prompts.extend([row[1] for row in rows])
        prompt_ids.extend([row[0] for row in rows])
        
    # Get prompts based on usage_to_query
    sql = f"select {name}_id, {name} from {name}_usage where usage_count = {usage_to_query} order by usage_count desc limit {usage_amount_to_get};"
    rows = db.execute(sql).fetchall()
    prompts.extend([row[1] for row in rows])
    prompt_ids.extend([row[0] for row in rows])
    
    return prompts, prompt_ids


def get_subjects(db, control):
    """Retrieves subjects from the database based on control."""
    subjects = []
    subject_ids = []
    name = "subject"
    
    # Get subjects based on rating from the database
    for rating, count in control["subjects"].items():
        # sql = f"SELECT subject_id, subject FROM subjects WHERE rating = {rating} AND status = 'open' ORDER BY RANDOM() LIMIT {count};"
        sql = f"select {name}_id, {name} from {name}_usage where rating = {rating} limit {count};"
        # sql = f"SELECT p.{name}_id, p.{name}, COUNT(u.item_id) AS usage_count FROM {name}s p LEFT JOIN usage u ON p.{name}_id = u.item_id WHERE p.status = 'open' and p.rating = {rating} and u.table_name = '{name}s' GROUP BY p.{name} ORDER BY usage_count ASC, RANDOM() LIMIT {count};"
        rows = db.execute(sql).fetchall()
        subjects.extend([row[1] for row in rows])
        subject_ids.extend([row[0] for row in rows])
        
    # Get subjects based on usage_to_query
    sql = f"select {name}_id, {name} from {name}_usage where usage_count = {usage_to_query} order by usage_count desc limit {usage_amount_to_get};"
    rows = db.execute(sql).fetchall()
    subjects.extend([row[1] for row in rows])
    subject_ids.extend([row[0] for row in rows])

    return subjects, subject_ids


def get_control(db):
    """Retrieves control data from the database."""
    control = {"styles": {}, "prompts": {}, "subjects": {}}
    for row in db.execute(
        "SELECT tablename, rating, count FROM control WHERE count > 0;"
    ):
        tablename, rating, count = row
        control[tablename][rating] = count
    return control


def replace_wildcards(db, prompts):
    """Replaces wildcards in prompts with random values from the database."""
    try:
        for i in range(len(prompts)):
            while re.search(r"\_\_(.+)\_\_", prompts[i]):
                match = re.search(r"\_\_(.+?)\__", prompts[i])
                wildcard = match.group(1)
                value = get_wildcard(db, wildcard)
                prompts[i] = re.sub(f"__{wildcard}__", value, prompts[i], 1)
        return prompts
    except Exception as e:
        logging.error(f"Error replacing wildcards: {e}")
        return prompts


def get_wildcard(db, wildcard):
    """Retrieves a random value for the given wildcard from the database."""
    try:
        sql = f"SELECT value FROM wildcards WHERE wildcard = '{wildcard}' ORDER BY RANDOM() LIMIT 1;"
        value = db.execute(sql).fetchone()[0]
        return value
    except Exception as e:
        logging.error(f"Error getting wildcard value {wildcard}: {e}")
        return None

def clear_prompt_temp(db):
    # Delete existing data
    cursor = db.cursor()
    table_name = "prompts_tmp"
    try:
        cursor.execute(f"DELETE FROM {table_name}")
    except sqlite3.Error as e:
        logging.error(f"Error clearing existing data from {table_name}: {e}")
        return

def save_prompts(db, prompts):
    table_name = "prompts_tmp"
    cursor = db.cursor()
    columns = "prompts"
    placeholders = "?"


    data = [(prompt,) for prompt in prompts]
    # pprint.pprint(data)

    try:
        cursor.executemany(
            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
            data,
        )
    except sqlite3.Error as e:
        logging.error(f"An error occurred while inserting data into {table_name}: {e}")

    db.commit()

def save_to_text(prompts):
    date_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{date_str}.txt"

    with open(filename, "w") as f:
        for prompt in prompts:
            f.write(f"{prompt}\n")

def save_usage(db, style_ids, prompt_ids, subject_ids):
    table_name = "usage"
    cursor = db.cursor()
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
    

def run():
    prefix = config.prompt_prefix
    suffix = config.prompt_suffix

    logging.info("get_prompts : start")

    try:
        db = sqlite3.connect(config.DB_NAME)
        control = get_control(db)

        subjects, subject_ids = get_subjects(db, control)
        styles, style_ids = get_styles(db, control)
        prompts, prompt_ids = get_prompts(db, control)
        
        # Add prompt IDs to each prompt string
        prompts = [f"{prompt} p{prompt_ids[i]}" for i, prompt in enumerate(prompts)]

        prompts.extend(combine_subjects(subjects, styles, subject_ids, style_ids))

        if prefix:
            prompts = [f"{prefix} {x}" for x in prompts]

        if suffix:
            prompts = [f"{x} {suffix}" for x in prompts]

        prompts = replace_wildcards(db, prompts)

        logging.info(f"get_prompts : {len(prompts)} : prompts built")

        clear_prompt_temp(db)
        save_prompts(db, prompts)
        #save_usage(db, style_ids, prompt_ids, subject_ids)
        if config.save_prompts_to_txt:
            save_to_text(prompts)

        logging.info("get_prompts : complete")

    except Exception as e:
        logging.error(f"Error occurred: {e}")

    finally:
        if db:
            db.close()

def main():
    run()

if __name__ == "__main__":
    main()
