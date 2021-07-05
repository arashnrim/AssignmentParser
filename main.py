import os
import argparse
import json
import uuid
import time
import requests
from dotenv import load_dotenv
from dateutil.parser import parse

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
AP_PARSER = argparse.ArgumentParser()
AP_PARSER.add_argument("-i", "--input", help="the input file with the homework list", dest="input")
AP_PARSER.add_argument("-t", "--type", help="the file type of the input file; default is txt", dest="type")
AP_ARGS = AP_PARSER.parse_args()

input_type = AP_ARGS.type if AP_ARGS.type else "txt"
input_file = AP_ARGS.input if AP_ARGS.input else "{}/input.{}".format(ROOT_DIR, input_type)

class MissingInputFileError(Exception):
    """An exception to handle the missing input file."""
class EmptyInputFileError(Exception):
    """An exception to hadle an empty input file."""
class MissingSecretError(Exception):
    """An exception to handle the missing .env file."""

def parse_task(line):
    """
    Receives a line and parses it to match the format `[subject] name`, where `subject` is a two-letter code for the subject and `name` is the name of the task.

    If `subject` is invalid, the user is re-prompted until a valid entry is given. Capitalisation is automatic.

    Args:
        line: A line to parse a task from.

    Returns:
        A string with the format `[subject] name`, explained above.
    """
    subject, name = line.split(" - ")
    print("Parsing {}...".format(line))

    while not subject.isupper() or not len(subject) == 2:
        subject = input("The subject {} does not meet your standarised format. What should be the corrected term? ".format(subject)).upper()

    return "[{}] {}".format(subject, name)

def parse_tasks(lines):
    """
    Receives lines and parses them into a dictionary of tasks.

    Args:
        lines: The lines to parse.

    Returns:
        A dictionary in the format `{ date: tasks }`, where `date` is a `datetime.datetime` type and `tasks` is a list.
    """
    grouped_tasks = {}
    due_parsed = ""
    i_tasks = []
    for line in lines:
        try:
            new_due = parse(line)
        except ValueError:
            i_tasks.append(parse_task(line))
        else:
            grouped_tasks[due_parsed] = i_tasks
            i_tasks = []
            due_parsed = new_due
        grouped_tasks[due_parsed] = i_tasks
    if not grouped_tasks[""]:
        del grouped_tasks[""]
    return grouped_tasks

def create_task(due, name):
    """
    Creates the task on Todoist using its API.

    Args:
        due: The due date of the task.
        name: The name of the task.
    """
    print("Sending \"{}\"...".format(name), end="\r")

    response = requests.post(
        "https://api.todoist.com/rest/v1/tasks",
        data=json.dumps({
            "content": name,
            "due_date": due.strftime("%Y-%m-%d"),
            "project_id": 2268855166
        }),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer {}".format(os.getenv("TODOIST_KEY"))
        }
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Sending \"{}\"... Error".format(name))
    else:
        print("Sending \"{}\"... OK".format(name))

try:
    with open(input_file):
        pass
except Exception as e:
    raise MissingInputFileError("The specified input file was not found.") from e
else:
    with open(input_file) as file:
        lines = [line.strip("\n") for line in file.readlines() if line.strip("\n")]
    if not lines:
        raise EmptyInputFileError("The input file is empty.")
    if not os.getenv("TODOIST_KEY"):
        raise MissingSecretError("The TODOIST_KEY secret was not found.")
    tasks = parse_tasks(lines)
    print()
    for due, assignments in tasks.items():
        for assignment in assignments:
            create_task(due, assignment)

    print("\nProgram completed. Clearing input file...", end="\r")
    with open(input_file, "w"):
        pass
    time.sleep(2)
    print("Program completed. Clearing input file... OK", end="\r")
    time.sleep(2)
    print("Program completed.")
