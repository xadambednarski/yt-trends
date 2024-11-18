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


def save_videos(videos: list[Video], range_channels: int, path: str = None):
    if path is None:
        path = f"data/videos/videos_{str(range_channels[0])}-{str(range_channels[1])}.json"
    if not videos:
        logging.info(f"No videos to save, range: {str(range_channels)}")
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


def get_videos(api: YoutubeAPI, channel_id: list[dict], num_videos: int, country: str):
    videos_list = []
    videos = api.get_top_videos(channel_id, num_videos)
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
            date,
            country
        )
        videos_list.append(video)
        print("Video: ", video.title)
    logging.info(f"Videos retrieved for channel {author}.")
    return videos_list


def get_videos_for_country(
    api: YoutubeAPI, range_channels: list[int], country: str, num_videos: int = 50
):
    global CATEGORIES
    if not range_channels:
        logging.info("No channels to update.")
        return
    logging.info(f"Updating videos for {country}...")
    channels = load_channels(country)
    errors_num = 0
    idx_start = range_channels[0] - 1
    CATEGORIES = api.get_categories(country)
    all_videos = []
    while idx_start < range_channels[1]:
        try:
            channel_id = channels[idx_start]["id"]
            print("Channel: ", channels[idx_start]["name"])
            channel_videos = get_videos(api, channel_id, num_videos, country)
            if channel_videos:
                all_videos.extend(channel_videos)
            idx_start += 1
        except Exception:
            if errors_num == 3:
                logging.info(
                    "Error: too many errors, stopping the process. Please try again later."
                )
                save_videos(all_videos, country, range_channels)
                return
            logging.info(
                f"Error: retrieving data for channel {channels[idx_start]['name']}, retrying..."
            )
            time.sleep(3)
            errors_num += 1
            continue


def main():
    api = YoutubeAPI()
    channels_range = [1, 1000]
    get_videos_for_country(api, channels_range, "united-states", num_videos=50)


if __name__ == "__main__":
    main()
