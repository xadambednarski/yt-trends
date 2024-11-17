import os
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
from typing import Literal, Union
import configparser
import requests
import enum
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
config = configparser.ConfigParser()
config.read("config/config.ini")

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"


class ThumbnailSize(enum.Enum):
    MAXRES = "maxres"
    HIGH = "high"
    MEDIUM = "medium"
    DEFAULT = "default"
    STANDARD = "standard"

    def __str__(self):
        return self.name


class YoutubeAPI:
    def __init__(self):
        self.config_file = config["API"]["CONFIG_FILE"]
        credentials = service_account.Credentials.from_service_account_file(
            self.config_file, scopes=scopes
        )
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials
        )

    def get_channel(self, channel_id: str) -> dict[str, Union[str, dict[str, str]]]:
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics", id=channel_id
        )
        response = request.execute()
        return response

    def get_channel_by_name(self, channel_name: str) -> dict[str, Union[str, dict[str, str]]]:
        request = self.youtube.search().list(part="snippet", q=channel_name, type="channel")
        response = request.execute()
        return response

    def get_playlist(self, playlist_id: str) -> dict[str, Union[str, dict[str, str]]]:
        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails", playlistId=playlist_id
        )
        response = request.execute()
        return response

    def get_video(self, video_id: str) -> dict[str, Union[str, dict[str, str]]]:
        request = self.youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
        response = request.execute()
        return response

    def get_thumbnail(
        self,
        video,
        resolution: Literal[
            ThumbnailSize.DEFAULT,
            ThumbnailSize.STANDARD,
            ThumbnailSize.MEDIUM,
            ThumbnailSize.HIGH,
            ThumbnailSize.MAXRES,
        ] = ThumbnailSize.DEFAULT,
        getsize: bool = False,
    ) -> Union[str, tuple[str, tuple[int, int]]]:
        """
        Retrieves the thumbnail of a video

        Notes:
        - getsize is a boolean indicating if the size of the thumbnail should be returned

        Returns:
        - url (str) - The URL of the thumbnail
        - size (tuple) - The size of the thumbnail (width, height)
        """
        thumbnail = video["items"][0]["snippet"]["thumbnails"][resolution.value]
        try:
            size = (
                thumbnail["width"],
                thumbnail["height"],
            )
        except KeyError:
            size = None
        return thumbnail["url"], size if getsize else thumbnail["url"], None

    def get_video_description(self, video: dict[str, Union[str, dict[str, str]]]) -> str:
        """
        Retrieves the description of a video
        """
        return video["items"][0]["snippet"]["description"]

    def get_video_category(self, video: dict[str, Union[str, dict[str, str]]]) -> str:
        """
        Retrieves the category of a video (e.g. Music, Entertainment, etc.)
        """
        category_id = video["items"][0]["snippet"]["categoryId"]
        request = self.youtube.videoCategories().list(part="snippet", id=category_id)
        response = request.execute()
        return response["items"][0]["snippet"]["title"]

    def get_channel_category(self, channel: dict[str, Union[str, dict[str, str]]]) -> str:
        """
        Retrieves the category of a channel (e.g. Music, Entertainment, etc.)
        """
        category_id = channel["items"][0]["snippet"]["categoryId"]
        return category_id

    def get_video_stats(self, video: dict[str, Union[str, dict[str, str]]]) -> dict[str, int]:
        """
        Retrieves the statistics of a video:
        - viewCount (int) - The number of times the video has been viewed
        - likeCount (int) - The number of times the video has been liked
        - favoriteCount (int) - The number of times the video has been added to a user's favorites
        - commentCount (int) - The number of comments on the video
        """
        stats = video["items"][0]["statistics"]
        return stats

    def get_top_videos(self, channel_id: str, num_videos: int = 10):
        request = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=num_videos,
            order="viewCount",
            type="video",
        )
        response = request.execute()
        return response

    def get_last_channel_videos(
        self, channel_id: str, num_videos: int = 10
    ) -> dict[str, Union[str, dict[str, str]]]:
        """
        Retrieves the last {num_videos} videos from a channel
        """
        request = self.youtube.search().list(
            part="snippet", channelId=channel_id, maxResults=num_videos, order="date", type="video"
        )
        response = request.execute()
        return response

    def get_channel_videos_timerange(self, channel_id: str, start_time: str, end_time: str):
        """
        Retrieves the videos from a channel within a time range

        Notes:
        - The time range is in the format "YYYY-MM-DDTHH:MM:SSZ" (e.g. "2021-01-01T00:00:00Z")
        """
        request = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            publishedAfter=start_time,
            publishedBefore=end_time,
            type="video",
        )
        response = request.execute()
        return response

    def get_youtube_categories(self, region_code: str = "US"):
        """
        Retrieves the list of categories available on YouTube
        """
        request = self.youtube.videoCategories().list(part="snippet", regionCode=region_code)
        response = request.execute()
        categories = {}
        for item in response["items"]:
            categories[item["id"]] = item["snippet"]["title"]
        return categories

    def get_channel_thumbnail(
        self,
        channel: dict[str, Union[str, dict[str, str]]],
        resolution: Literal[
            ThumbnailSize.DEFAULT,
            ThumbnailSize.STANDARD,
            ThumbnailSize.MEDIUM,
            ThumbnailSize.HIGH,
            ThumbnailSize.MAXRES,
        ] = ThumbnailSize.DEFAULT,
        getsize: bool = False,
    ) -> str:
        """
        Retrieves the thumbnail of a channel
        """
        thumbnail = channel["items"][0]["snippet"]["thumbnails"][resolution.value]
        try:
            size = (
                thumbnail["width"],
                thumbnail["height"],
            )
        except KeyError:
            size = None
        return thumbnail["url"], size if getsize else thumbnail["url"], None


def show_thumbnail_from_url(url: str) -> None:
    response = requests.get(url)
    fig = plt.imshow(Image.open(BytesIO(response.content)))
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.show()
