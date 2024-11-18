from yt_api import YoutubeAPI, ThumbnailSize
import time
import json
import logging
from utils import Video
from main_channels import load_channels


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    filename="logs.log",
    encoding="utf-8",
)


def load_videos(channel_id: str, path: str = None) -> list[dict[str, str]]:
    if path is None:
        path = f"data/videos/videos_{channel_id}.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            videos = json.load(f)
        if not videos:
            logging.info(f"No videos found, channel: {channel_id}.")
            return []
        return videos
    except FileNotFoundError:
        return []
    except Exception as e:
        logging.error(f"Error loading videos: {e}")
        return []


def save_videos(videos: list[Video], channel_id: str, path: str = None):
    if path is None:
        path = f"data/videos/videos_{channel_id}.json"
    if not videos:
        logging.info(f"No videos to save, channel: {channel_id}.")
        return
    try:
        with open(path, "w", encoding="utf-8") as f:
            if isinstance(videos[0], Video):
                json.dump([video.__dict__ for video in videos], f, ensure_ascii=False, indent=4)
            else:
                json.dump(videos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Error saving videos: {e}")
        return


def get_videos(api: YoutubeAPI, channel_id: list[dict], start_time: str, end_time: str):
    videos_list = []
    try:
        videos = api.get_channel_videos_timerange(channel_id, start_time, end_time)
        if not videos:
            logging.info("No videos found.")
            return

        for video_data in videos:
            video_id = video_data["id"]
            title = video_data["snippet"]["title"]
            description = video_data["snippet"]["description"]
            category_id = video_data["snippet"]["categoryId"]
            category = CATEGORIES.get(category_id, "Unknown")
            thumbnail = api.get_thumbnail(video_data, ThumbnailSize.MAXRES)
            author = video_data["snippet"]["channelTitle"]
            stats = api.get_video_stats(video_data)
            date = video_data["snippet"]["publishedAt"]
            author_id = video_data["snippet"]["channelId"]
            video = Video(
                video_id,
                title,
                description,
                category,
                thumbnail,
                author,
                author_id,
                stats["viewCount"],
                stats["likeCount"],
                stats["commentCount"],
                date
            )
            videos_list.append(video)
            print("Video: ", video.title)

        logging.info(f"Videos retrieved for channel {author}.")
        save_videos(videos_list, channel_id)
        logging.info("All videos saved.")
    except Exception as e:
        logging.error(f"Error: {e}")
        return


def get_videos_for_country(
    api: YoutubeAPI, range_channels: list[int], country: str, start_time: str, end_time: str
):
    global CATEGORIES
    if not range_channels:
        logging.info("No channels to update.")
        return
    logging.info(f"Updating videos for {country}...")
    channels = load_channels(country)
    errors_num = 0
    idx_start = range_channels[0]
    CATEGORIES = api.get_categories(country)
    while idx_start < range_channels[1]:
        try:
            channel_id = channels[idx_start]["id"]
            print("Channel: ", channels[idx_start]["name"])
            get_videos(api, channel_id, start_time, end_time)
            idx_start += 1
        except Exception:
            if errors_num == 3:
                logging.info(
                    "Error: too many errors, stopping the process. Please try again later."
                )
                return
            logging.info(
                f"Error: retrieving data for channel {channels[idx_start]['name']}, retrying..."
            )
            time.sleep(3)
            errors_num += 1
            continue


def main():
    api = YoutubeAPI()
    range_channels = [0, 1]
    start_time = "2024-01-01T00:00:00Z"
    end_time = "2024-02-01T00:00:00Z"
    get_videos_for_country(api, range_channels, "united-states", start_time, end_time)


if __name__ == "__main__":
    main()
