import logging
import argparse
from concurrent.futures import ThreadPoolExecutor
from myBrowser.src.project.twitter_automation import TwitterAutomation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_task(task_type, **kwargs):
    if task_type == "twitter":
        return TwitterAutomation(**kwargs)
    else:
        raise ValueError(f"Unsupported task type: {task_type}")

def parse_task_args(task_args):
    tasks = []
    for arg in task_args:
        task_info = arg.split(':')
        task_type = task_info[0]
        # 解析范围
        index_range = task_info[1].split('-')
        start_index = int(index_range[0])
        end_index = int(index_range[1]) + 1  # 包括结束索引
        for index in range(start_index, end_index):
            task_kwargs = {'user_data_index': index}
            for kv in task_info[2:]:
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
    parser.add_argument('-t', '--tasks', nargs='+', action='append', help='Tasks with their parameters in task_type:index_range:key=value format', required=True)

    args = parser.parse_args()

    # Flatten the list of lists for tasks
    task_args = [item for sublist in args.tasks for item in sublist]
    tasks = parse_task_args(task_args)

    main(tasks)

