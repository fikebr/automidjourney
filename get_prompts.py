import sqlite3
import datetime
import pprint
import config
import re
import logging
from log import setup_logging

setup_logging()


def combine_subjects(subjects, styles):
    """Combines subjects and styles to create prompts."""
    prompts = []
    for subject in subjects:
        for style in styles:
            prompt = f"{subject} | in the style of {style}"
            prompts.append(prompt)
    return prompts


def get_styles(db, control):
    """Retrieves styles from the database based on control."""
    styles = []
    for rating, count in control["styles"].items():
        sql = f"SELECT style FROM styles WHERE rating = {rating} AND status = 'open' ORDER BY RANDOM() LIMIT {count};"
        rows = db.execute(sql).fetchall()
        styles.extend([row[0] for row in rows])
    return styles


def get_prompts(db, control):
    """Retrieves prompts from the database based on control."""
    prompts = []
    for rating, count in control["prompts"].items():
        sql = f"SELECT prompt FROM prompts WHERE rating = {rating} AND status = 'open' ORDER BY RANDOM() LIMIT {count};"
        rows = db.execute(sql).fetchall()
        prompts.extend([row[0] for row in rows])
    return prompts


def get_subjects(db, control):
    """Retrieves subjects from the database based on control."""
    subjects = []
    for rating, count in control["subjects"].items():
        sql = f"SELECT subject FROM subjects WHERE rating = {rating} AND status = 'open' ORDER BY RANDOM() LIMIT {count};"
        rows = db.execute(sql).fetchall()
        subjects.extend([row[0] for row in rows])
    return subjects


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


def run():
    prefix = config.prompt_prefix
    suffix = config.prompt_suffix

    logging.info("get_prompts : start")

    try:
        db = sqlite3.connect(config.DB_NAME)
        control = get_control(db)
        subjects = get_subjects(db, control)
        # pprint.pprint(subjects)
        styles = get_styles(db, control)
        prompts = get_prompts(db, control)

        prompts.extend(combine_subjects(subjects, styles))

        if prefix:
            prompts = [f"{prefix} {x}" for x in prompts]

        if suffix:
            prompts = [f"{x} {suffix}" for x in prompts]

        prompts = replace_wildcards(db, prompts)

        logging.info(f"get_prompts : {len(prompts)} : prompts built")

        clear_prompt_temp(db)
        save_prompts(db, prompts)

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
