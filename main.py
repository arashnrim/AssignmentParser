import os, argparse, requests, uuid, json
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

def parse_task(task):
    subject, assignment = task.split(" - ")
    print("Parsing {}...".format(task))

    while not(subject.isupper()) or not(len(subject) == 2):
        subject = input("The subject {} does not meet your standarised format. What should be the corrected term? ".format(subject)).upper()

    return "[{}] {}".format(subject, assignment)

def parse_tasks(lines):
    grouped_tasks = {}
    due = ""
    i_tasks = []
    for line in lines:
        try: new_due = parse(line)
        except ValueError: i_tasks.append(parse_task(line))
        else:
            grouped_tasks[due] = i_tasks
            i_tasks = []
            due = new_due
        grouped_tasks[due] = i_tasks
    if not grouped_tasks[""]: del grouped_tasks[""]
    return grouped_tasks

def create_task(due, assignment):
    print("Sending \"{}\"...".format(assignment), end="\r")

    response = requests.post(
        "https://api.todoist.com/rest/v1/tasks",
        data=json.dumps({
            "content": assignment,
            "due_date": due.strftime("%Y-%m-%d"),
            "project_id": 2268855166
        }),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer {}".format(os.getenv("TODOIST_KEY"))
        }
    )

    try: response.raise_for_status()
    except requests.exceptions.HTTPError: print("Sending \"{}\"... Error".format(assignment))
    else: print("Sending \"{}\"... OK".format(assignment))

try:
    open(input_file)
except FileNotFoundError: print("The specified input file was not found. Please try again!")
else:
    with open(input_file) as file:
        lines = [line.strip("\n") for line in file.readlines() if line.strip("\n")]
    tasks = parse_tasks(lines)
    print()
    for due, assignments in tasks.items():
        for assignment in assignments: create_task(due, assignment)
    
    print("\nProgram completed.")
