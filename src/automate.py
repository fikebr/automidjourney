import sqlite3
import pyautogui
import time
import os
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
import config
import random
import logging

pyautogui.FailSafeException = True

def get_prompts(db):
    cursor = db.cursor()

    sql = "select prompts from prompts_tmp ORDER BY RANDOM();"

    try:
        cursor.execute(sql)
        prompts = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        logging.error(f"Error occurred: {e}")

    return(prompts)


def automate_now(prompt):

    try:
        logging.info(
            f"automate : Prompt: {prompt}"
        )

        # pyautogui.click('promptbar.png')  # Click on the prompt bar (replace with actual coordinates if needed)
        x, y = pyautogui.locateCenterOnScreen(config.promptbar_image, confidence=0.9)
        pyautogui.click(x, y)
        pyautogui.write(prompt)
        pyautogui.press('enter')
    except Exception as e:
        logging.error("Error occurred during automate_now:")
        logging.error(f"  - Type: {type(e).__name__}")
        logging.error(f"  - Message: {str(e)}")
        logging.error(f"  - Arguments: {e.args}")
        logging.error(f"  - Traceback: {e.__traceback__}")


def run():
    logging.info("automate : start")
    if not os.path.exists(config.promptbar_image):
        logging.warn(
            f"automate : Could not find the promptbar image {config.promptbar_image}"
        )
        return

    try:
        db = sqlite3.connect(config.DB_NAME)
    except Exception as e:
        logging.error(f"Error occurred: {e}")

    prompts = get_prompts(db)
    db.close()

    prompts_count = len(prompts)
    prompts_curent = 1

    logging.info(f"automate : {prompts_count} prompts")

    for prompt in prompts:

        logging.info(f"automate : {prompts_curent} of {prompts_count} prompts")

        automate_now(prompt)
        prompts_curent = prompts_curent + 1

        sleep = random.randint(1, config.automate_sleep)
        sleep = sleep + config.automate_sleep

        logging.info(f"automate : sleeping for {sleep} seconds")

        time.sleep(sleep)

    logging.info("automate : complete")


def main():
    run()


if __name__ == "__main__":
    main()
