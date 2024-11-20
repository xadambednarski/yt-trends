from top_scraper import Scraper
from yt_api import YoutubeAPI, ThumbnailSize
import time
import json
import sys
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


def update_channels_info(api: YoutubeAPI, channels: dict, range=None) -> dict:
    if not range:
        return channels
    logging.info("Updating channels info...")
    errors_num = 0
    idx_start = range[0]
    while idx_start < range[1]:
        try:
            channel_data = api.get_channel_by_name(channels[idx_start]["name"])
            channel_id = channel_data["items"][0]["id"]
            channel_name = channel_data["items"][0]["snippet"]["title"]
            channel_description = channel_data["items"][0]["snippet"]["description"]
            channel_thumbnail = api.get_channel_thumbnail(channel_data, ThumbnailSize.HIGH)
            channels[idx_start]["id"] = channel_id
            channels[idx_start]["name"] = channel_name
            channels[idx_start]["description"] = channel_description
            channels[idx_start]["thumbnail"] = channel_thumbnail
            print(f"Channel {idx_start} updated.")
            idx_start += 1
        except Exception:
            if errors_num == 3:
                logging.info(
                    "Error: too many errors, stopping the process. Please try again later."
                )
                return channels
            logging.info(
                f"Error: retrieving data for channel {channels[idx_start]['name']}, retrying..."
            )
            time.sleep(3)
            errors_num += 1
            continue
    logging.info("Channels info updated.")
    return channels


def load_channels(country: str) -> list[dict]:
    logging.info(f"Loading top channels for {country}...")
    try:
        with open(f"data/channels/top_1000_{country}.json", "r", encoding="utf-8") as f:
            content = json.load(f)
            if not content:
                logging.info("Error: no channels found.")
                sys.exit(1)
            logging.info(f"Loaded {len(content)} channels.")
            return content
    except Exception as e:
        logging.info(f"Error: {e}")
        sys.exit(1)


def scrape_top_channels(country: str, path=None):
    if path is None:
        path = f"data/channels/top_1000_{country}.json"
    if not os.path.exists(path):
        logging.info(f"Scraping top channels for {country}...")
        scraper = Scraper(TOP_1000_COUNTRY.format(country=country), country)
        scraper.get_top_channels(scraper.url)
        if scraper.channels and len(scraper.channels) > 0:
            save_channels(country, scraper.channels, path)
            return scraper.channels
        else:
            logging.info("Error: no channels found.")
            sys.exit(1)
    else:
        try:
            top_channels = load_channels(country)
        except Exception as e:
            logging.info(f"Error: {e}")
            sys.exit(1)
        if top_channels and len(top_channels) > 0:
            return top_channels
        else:
            logging.info("Error: no channels found.")
            sys.exit(1)


def save_channels(country, channels, path=None) -> None:
    if path is None:
        path = f"data/top_1000_{country}.json"
    with open(path, "w", encoding="utf-8") as f:
        logging.info(f"Saving top channels for {country}...")
        if not channels:
            logging.info("Error: no channels found.")
            sys.exit(1)
        else:
            try:
                json.dump(
                    [channel.__dict__ for channel in channels], f, ensure_ascii=False, indent=4
                )
            except AttributeError:
                json.dump(channels, f, ensure_ascii=False, indent=4)


def main():
    top_poland_path = "data/channels/top_1000_poland.json"
    top_usa_path = "data/channels/top_1000_united-states.json"

    top_channels_pl = scrape_top_channels("poland", path=top_poland_path)
    top_channels_usa = scrape_top_channels("united-states", path=top_usa_path)

    yt_api = YoutubeAPI()
    top_channels_pl = update_channels_info(yt_api, top_channels_pl, range=(997, 1000))
    top_channels_usa = update_channels_info(yt_api, top_channels_usa)

    save_channels("poland", channels=top_channels_pl, path=top_poland_path)
    save_channels("usa", top_channels_usa, path=top_usa_path)


if __name__ == "__main__":
    main()
