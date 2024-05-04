import csv
import argparse
from concurrent.futures import ThreadPoolExecutor
from myBrowser.src.project.twitter_automation import TwitterAutomation
from src.utils.config_loader import get_config_path

def create_task(task_type, **kwargs):
    if task_type == "twitter":
        return TwitterAutomation(**kwargs)

    else:
        raise ValueError(f"Unsupported task type: {task_type}")

def load_tasks_from_csv(file_path):
    tasks = []
    file_path = get_config_path(file_path)
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task_type = row.pop('task_type')
            tasks.append(create_task(task_type, **row))
    return tasks

def parse_task_args(task_args):
    tasks = []
    for arg in task_args:
        task_info = arg.split(':')
        task_type = task_info[0]
        task_kwargs = {}
        for kv in task_info[1:]:
            key, value = kv.split('=')
            task_kwargs[key] = value
        tasks.append(create_task(task_type, **task_kwargs))
    return tasks

def main(tasks):
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = [executor.submit(task.run) for task in tasks]

        for future in futures:
            result = future.result()
            print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Social Media Automation Script')
    parser.add_argument('-f', '--file', help='Path to the CSV file containing task data', required=False)
    parser.add_argument('-t', '--tasks', nargs='+', action='append', help='Tasks with their parameters in task_type:key=value format', required=False)

    args = parser.parse_args()

    tasks = []

    if args.file:
        tasks.extend(load_tasks_from_csv(args.file))

    if args.tasks:
        # Flatten the list of lists for tasks
        task_args = [item for sublist in args.tasks for item in sublist]
        tasks.extend(parse_task_args(task_args))

    if not tasks:
        print("No tasks to execute. Please provide tasks through -f/--file or -t/--tasks.")
    else:
        main(tasks)

