import selenium
from selenium.webdriver.common.by import By
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from utils import Channel


options = Options()
options.add_argument("--headless")


class Scraper:
    def __init__(self, url: str, country: str):
        self.url = url
        self.country = country
        self.driver = selenium.webdriver.Chrome(options=options)
        self.channels: list[Channel] = []

    def get_top_channels(self, url: str) -> None:
        self.driver.get(url)
        table = self.driver.find_element(by=By.TAG_NAME, value="tbody")
        rows = table.find_elements(by=By.TAG_NAME, value="tr")
        for row in rows[1:]:
            cells = row.find_elements(by=By.TAG_NAME, value="td")
            rank = int(cells[0].text)
            name = cells[1].find_element(by=By.TAG_NAME, value="a").text
            channel = Channel(name, rank)
            self.channels.append(channel)
