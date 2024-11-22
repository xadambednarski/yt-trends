import json
import logging
import sys
import os
from typing import Optional, List, Dict
from dataclasses import dataclass

from yt_api import YoutubeAPI, ThumbnailSize
from scrape_top_channels import Scraper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename="logs.log",
    encoding="utf-8",
)

TOP_1000_URL_TEMPLATE = (
    "https://us.youtubers.me/{country}/all/top-1000-most-subscribed-youtube-channels-in-{country}"
)


@dataclass
class Video:
    video_id: str
    title: str
    description: str
    category: str
    thumbnail: str
    author: str
    author_id: str
    views: int
    likes: int
    comments: int
    date: str

    def __str__(self):
        return f"{self.author} - {self.title}"


def load_json(file_path: str) -> List[Dict]:
    """Load JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data:
                raise ValueError("File is empty.")
            return data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Error loading JSON from {file_path}: {e}")
    return []


def save_json(data: List[Dict], file_path: str) -> None:
    """Save data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Data saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving data to {file_path}: {e}")


def scrape_channels(country: str, scraper: Scraper, path: str) -> List[Dict]:
    """Scrape and save top channels for a country."""
    if os.path.exists(path):
        logging.info(f"Channels data already exists: {path}")
        return load_json(path)

    logging.info(f"Scraping top channels for {country}...")
    scraper.get_top_channels(scraper.url)
    if scraper.channels:
        save_json([channel.__dict__ for channel in scraper.channels], path)
        return [channel.__dict__ for channel in scraper.channels]
    else:
        logging.error("No channels found during scraping.")
        return []


def update_channels(
    api: YoutubeAPI, channels: List[Dict], idx_range: Optional[range] = None
) -> List[Dict]:
    """Update channels with detailed information from YouTube API."""
    if not idx_range:
        return channels

    logging.info(f"Updating channel info for range: {idx_range}")
    for idx in idx_range:
        try:
            channel = channels[idx]
            channel_data = api.get_channel_by_name(channel["name"])
            item = channel_data["items"][0]
            channel.update(
                id=item["id"],
                name=item["snippet"]["title"],
                description=item["snippet"]["description"],
                thumbnail=api.get_channel_thumbnail(channel_data, ThumbnailSize.HIGH),
            )
            logging.info(f"Updated channel: {channel['name']}")
        except Exception as e:
            if "No more API credentials available." in str(e):
                logging.error("No more API credentials available. Exiting...")
                break
            logging.error(f"Error updating channel {channels[idx]['name']}: {e}")
    return channels


def get_videos(api: YoutubeAPI, channel_id: str, num_videos: int) -> List[Video]:
    """Fetch top videos for a given channel."""
    try:
        videos_data = api.get_last_videos(channel_id, num_videos)
        return [
            Video(
                video_id=video["id"],
                title=video["snippet"]["title"],
                description=video["snippet"]["description"],
                category=video["snippet"]["categoryId"],
                thumbnail=api.get_thumbnail(video, ThumbnailSize.HIGH),
                author=video["snippet"]["channelTitle"],
                author_id=video["snippet"]["channelId"],
                views=int(video["statistics"].get("viewCount", 0)),
                likes=int(video["statistics"].get("likeCount", 0)),
                comments=int(video["statistics"].get("commentCount", 0)),
                date=video["snippet"]["publishedAt"],
            )
            for video in videos_data
        ]
    except Exception as e:
        logging.error(f"Error fetching videos for channel {channel_id}: {e}")
        return []


def save_progress(progress_path: str, progress: Dict) -> None:
    """Save scraping progress to a JSON file."""
    try:
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=4)
        logging.info(f"Progress saved to {progress_path}")
    except Exception as e:
        logging.error(f"Error saving progress to {progress_path}: {e}")


def load_progress(progress_path: str) -> Dict:
    """Load scraping progress from a JSON file."""
    if os.path.exists(progress_path):
        try:
            with open(progress_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading progress from {progress_path}: {e}")
    return {"last_processed_idx": 0}


def get_progress_path(country: str, type="last") -> str:
    """Get the progress file path for a specific country."""
    return os.path.join("data", "videos", type, country, "progress.json")


def process_videos(
    yt_api: YoutubeAPI,
    channels: List[Dict],
    output_dir: str,
    batch_size: int,
    progress: Dict,
    progress_path: str,
) -> None:
    """Fetch and save videos for channels in batches."""
    last_idx = progress.get("last_processed_idx", 0)
    total_channels = len(channels)

    for start_idx in range(last_idx, total_channels, batch_size):
        end_idx = min(start_idx + batch_size, total_channels)
        batch_channels = channels[start_idx:end_idx]

        video_data = []
        for channel in batch_channels:
            try:
                videos = get_videos(yt_api, channel["id"], num_videos=50)
                video_data.append(
                    {"channel": channel, "videos": [video.__dict__ for video in videos]}
                )
                logging.info(f"Fetched {len(videos)} videos for channel {channel['name']}")
            except Exception as e:
                if "quotaExceeded" in str(e):
                    logging.error("Quota exceeded. Saving progress and exiting.")
                    progress["last_processed_idx"] = start_idx
                    save_progress(progress_path, progress)
                    return
                logging.error(f"Error fetching videos for channel {channel['name']}: {e}")

        output_file = os.path.join(output_dir, f"{start_idx + 1} - {end_idx}.json")
        save_json(video_data, output_file)

        progress["last_processed_idx"] = end_idx
        save_progress(progress_path, progress)

    logging.info("All videos processed successfully.")
    progress["last_processed_idx"] = total_channels
    save_progress(progress_path, progress)


def main():
    yt_api = YoutubeAPI()
    countries = ["poland", "united-states"]
    batch_size = 50

    for country in countries:
        channels_file = f"data/channels/top_1000_{country}.json"
        output_dir = os.path.join("data", "videos", "last", country)
        os.makedirs(output_dir, exist_ok=True)

        progress_path = get_progress_path(country)
        os.makedirs(os.path.dirname(progress_path), exist_ok=True)

        channels = load_json(channels_file)
        progress = load_progress(progress_path)

        process_videos(yt_api, channels, output_dir, batch_size, progress, progress_path)


if __name__ == "__main__":
    main()