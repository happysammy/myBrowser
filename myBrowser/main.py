import logging
from concurrent.futures import ThreadPoolExecutor
from myBrowser.src.project.twitter_automation import TwitterAutomation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # 定义任务列表
    tasks = [
        TwitterAutomation(username="user1", password="pass1"),
        TwitterAutomation(username="user2", password="pass2"),
        # 可以添加更多任务，甚至是不同类型的任务
    ]

    # 使用ThreadPoolExecutor并行执行任务
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = [executor.submit(task.run) for task in tasks]

        # 等待所有任务完成
        for future in futures:
            result = future.result()  # 如果有返回值可以在这里获取
            print(result)

if __name__ == "__main__":
    main()

