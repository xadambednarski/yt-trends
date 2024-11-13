from top_scraper import Scraper
from yt_api import YoutubeAPI, ThumbnailSize
import time
import json
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename="logs.log",
    encoding="utf-8",
)


TOP_1000_COUNTRY = (
    "https://us.youtubers.me/{country}/all/top-1000-most-subscribed-youtube-channels-in-{country}"
)


def update_channels_info(channels):
    for idx in range(len(channels)):
        while True:
            try:
                channel_data = yt_api.get_channel_by_name(channel_name=channels[idx]["name"])
                channel_id = channel_data["items"][0]["id"]["channelId"]
                channel_region_code = channel_data["regionCode"]
                channel_name = channel_data["items"][0]["snippet"]["title"]
                channel_description = channel_data["items"][0]["snippet"]["description"]
                channel_thumbnail = yt_api.get_channel_thumbnail(channel_id, ThumbnailSize.MAXRES)
                channels[idx]["url"] = channel_id
                channels[idx]["region_code"] = channel_region_code
                channels[idx]["name"] = channel_name
                channels[idx]["description"] = channel_description
                channels[idx]["thumbnail"] = channel_thumbnail
                time.sleep(1)
            except Exception as e:
                logging.info(
                    f"Error: retrieving data for channel {channels[idx]["name"]} - {e}, retrying..."
                )
                time.sleep(3)
                continue
    return channels


def load_channels(country: str):
    logging.info(f"Loading top channels for {country}")
    with open(f"data/top_1000_{country}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def scrape_top_channels(country: str):
    if not os.path.exists(f"data/top_1000_{country}.json"):
        logging.info(f"Scraping top channels for {country}")
        scraper = Scraper(TOP_1000_COUNTRY.format(country=country), country)
        top_channels = scraper.get_top_channels(scraper.url)
        save_channels(country, top_channels)
    else:
        top_channels = load_channels(country)
    return top_channels


def save_channels(country, channels, filename=None) -> None:
    if filename is None:
        filename = f"top_1000_{country}.json"
    with open(f"../data/{filename}", "w", encoding="utf-8") as f:
        logging.info(f"Saving top channels for {country}")
        json.dump([channel.__dict__ for channel in channels], f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    top_channels_pl = scrape_top_channels("poland")
    top_channels_usa = scrape_top_channels("united-states")

    yt_api = YoutubeAPI()
    logging.info("Updating channel information for top channels in Poland.")
    top_channels_pl = update_channels_info(top_channels_pl)
    logging.info("Updating channel information for top channels in USA.")
    top_channels_usa = update_channels_info(top_channels_usa)

    save_channels("poland", top_channels_pl, filename="top_1000_poland_updated.json")
    save_channels("usa", top_channels_usa, filename="top_1000_united-states_updated.json")
