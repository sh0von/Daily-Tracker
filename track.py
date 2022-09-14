from pathlib import Path, PurePath
from datetime import datetime, timezone, date
import json
import sys
import pytz
import re
import getpass
from sys import platform
import os
import xdrlib
from xml.sax import xmlreader

def configs(config_default_path, force_flag):
    # SET GLOBAL VARS
    if (force_flag or not Path(config_default_path).exists()):
        if not force_flag:
            print("The directory path for notes is missing")
        tmp_notes_dir = str(input("Please enter directory path for notes: "))
        with open(config_default_path, "w") as tf:
            tf.write(tmp_notes_dir)
    # Directory where note files will be saved
    with open(config_default_path, "r") as tf:
        global NOTES_DIR
        NOTES_DIR = tf.readline()
        
x=os.getcwd()
# CHECK OS3
def check_os(flag):
    if platform == "linux" or platform == "linux2":
        configs(f"{x}/Tracker.cfg", flag)
    elif platform == "win32":
        configs(f"{x}/Tracker.cfg", flag)

check_os(False)

# Set Paths & Dirs
Path(NOTES_DIR).mkdir(parents=True, exist_ok=True)
NOTES_DIR = Path(NOTES_DIR)

today= date.today()
# Get current time
tz_BD = pytz.timezone('Asia/Dhaka') 
datetime_BD = datetime.now(tz_BD)
DATETIME = datetime_BD.strftime("%H:%M:%S")
DATE = datetime_BD.strftime("%d/%m/%y")
# File for saving notes will be saved
FILE_PATH = PurePath(NOTES_DIR, f"note.json")
# Boilerplate
BOILERPLATE = {"notes": []}
BOILERPLATE = {"days": []}


def save_note(note):
    notes_data = []
    with open(FILE_PATH, 'r') as f:
        notes_data = json.load(f)
    # append to notes data
    notes_data['notes'].append({"day":DATE,"time":DATETIME, "note": note})
    with open(FILE_PATH, 'w') as f:
        json.dump(notes_data, f, indent=True)


def get_notes(target_date):
    if(Path(PurePath(NOTES_DIR, f"note.json")).exists()):
        print(f"###### SHOWING NOTES ######")
        with open(PurePath(NOTES_DIR, f"note.json"), "r") as f:
            n_data = json.load(f)
            for i in n_data['notes']:
                print(f"{i['day']}\t{i['time']}\t{i['note']}")
    else:
        print(f"------ No file given  :( ------")


def search(search_key):
    for i in Path(NOTES_DIR).iterdir():
        if(i.is_file()):
            with open(i) as f:
                for x in json.load(f)['notes']:
                    results = re.findall(f".*{search_key}.*", x['note'])
                    if results:
                        for r in results:
                            print(f"{x['day']}\t{x['time']}\t{r}")

def helper():
    print("Daily Tracker is a python based note taking utility")
    print("USAGE:\n")
    print("--help or --h                        Shows help")
    print("--note or --n                        Shows all notes")
    print("--search or --s \"Some text here\"     Search for a particular string in notes")


def main():
    # Get text from argv
    if len(sys.argv) >= 2 and (sys.argv[1] == "--note" or sys.argv[1] == "--n" or sys.argv[1] == "--date" or sys.argv[1] == "--d" or sys.argv[1] == "--search" or sys.argv[1] == "--s" or sys.argv[1] == "--help" or sys.argv[1] == "--h"):
        if sys.argv[1] == "--help" or sys.argv[1] == "--h":
            helper()
        elif len(sys.argv) == 3 and (sys.argv[1] == "--search" or sys.argv[1] == "--s"):
            if (len(sys.argv) > 3):
                print(
                    "------ Daily Tracker ------\nError!\nSearch string should be inside inverted commas")
                print(
                    "Example:   Daily Tracker --search \"Some text here\"    or    Daily Tracker --s \"Some text here\"")
            else:
                search(sys.argv[2].strip(" "))
                
        elif sys.argv[1] == "--note" or sys.argv[1] == "--n":
            get_notes(datetime.now().strftime('%Y-%m-%d'))
                            
    elif len(sys.argv) >= 2 and len(sys.argv[1]) != 0:
        txt = ""
        for word in sys.argv[1:]:
            txt += f"{word} "
            # Check & create file
            pass
        if (Path(FILE_PATH).exists()):
            save_note(txt)
            print("Note saved :)")
        else:
            tmp_file = open(FILE_PATH, "w")
            json.dump(BOILERPLATE, tmp_file)
            tmp_file.close()
            save_note(txt)
            print("Note saved :)")
    else:
        helper()


if __name__ == "__main__":
    try:
        main()
    except:
        print("------- Daily Tracker -------")
        helper()
