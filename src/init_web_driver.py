import os

from fake_useragent import UserAgent
from selenium import webdriver


def init_web_driver():
    ua = UserAgent()
    userAgent = ua.random
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    options.add_argument("--headless")
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')
    options.add_argument("--disable-extensions")
    options.add_argument('window-size=1920x1080');
    options.add_argument(f'user-agent={userAgent}')
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    chrome_driver = 'E:\Git Repos\web-scrapping-python\src/drivers/chromedriver.exe'
    os.environ['webdriver.chrome.driver'] = chrome_driver

    driver = webdriver.Chrome(options=options, executable_path=chrome_driver)

    return driver