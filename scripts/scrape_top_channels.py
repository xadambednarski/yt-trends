from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
from typing import List, Optional

options = Options()
options.add_argument("--headless")


@dataclass
class Channel:
    name: str
    rank: int
    id: Optional[str] = None
    thumbnail: Optional[str] = None
    description: Optional[str] = None


class Scraper:
    def __init__(self, url: str, country: str):
        self.url = url
        self.country = country
        self.driver = webdriver.Chrome(options=options)
        self.channels: List[Channel] = []

    def get_top_channels(self) -> None:
        """
        Scrapes the top channels from the webpage and stores them in `self.channels`.
        """
        try:
            self.driver.get(self.url)
            table = self.driver.find_element(By.TAG_NAME, "tbody")
            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                rank = int(cells[0].text.strip())
                name = cells[1].find_element(By.TAG_NAME, "a").text.strip()
                self.channels.append(Channel(name=name, rank=rank))
        except Exception as e:
            print(f"Error while scraping: {e}")
        finally:
            self.driver.quit()

    def get_channels(self) -> List[Channel]:
        """
        Returns the list of scraped channels.
        """
        return self.channels
