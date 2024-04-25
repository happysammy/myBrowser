from myBrowser.src.project.browser_manager import BrowserManager
class TwitterAutomation(BrowserManager):

    def __init__(self, username, password, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.password = password
    def login(self):
        self.driver.get("https://twitter.com/login")
        # 逻辑代码填充：查找输入框，输入用户名和密码，点击登录按钮等

    def run(self):
        self.start()
        self.login()
        self.close()
