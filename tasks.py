from robocorp.tasks import task
from robocorp import browser

@task
def robot_scrape_news():
    browser.configure(
        slowmo=100
    )
    open_news()


def open_news():
    browser.goto('https://gothamist.com/')

def search_anything():
    page = browser.page()
    