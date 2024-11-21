import os
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
from typing import Literal, Union, List, Dict
import requests
import enum
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


class ThumbnailSize(enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    DEFAULT = "default"
    STANDARD = "standard"

    def __str__(self):
        return self.name


class YoutubeAPI:
    def __init__(self):
        self.config_files = [
            f"config/{file}"
            for file in os.listdir("config/")
            if file.endswith(".json")
        ]
        self.current_config_index = 0
        self.youtube = self._initialize_api()

    def _initialize_api(self):
        """
        Initialize the YouTube API with the current service account configuration.
        """
        credentials = service_account.Credentials.from_service_account_file(
            self.config_files[self.current_config_index], scopes=SCOPES
        )
        return googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=credentials, cache_discovery=False
        )

    def _switch_credentials(self):
        """
        Switch to the next file with API credentials when the quota is exceeded. In case
        there are no more files, finish the program and save the data.
        """
        self.current_config_index += 1
        if self.current_config_index >= len(self.config_files):
            raise Exception("No more API credentials available.")
        self.youtube = self._initialize_api()

    def _execute_request(self, request):
        """
        Execute an API request and handle quota errors by rotating credentials.
        """
        try:
            return request.execute()
        except googleapiclient.errors.HttpError as e:
            if "quotaExceeded" in str(e):
                print("Quota exceeded. Switching to next API credentials...")
                self._switch_credentials()
                return self._execute_request(request)
            else:
                raise

    def get_channel(self, channel_id: str) -> Dict:
        request = self.youtube.channels().list(part="snippet", id=channel_id)
        return self._execute_request(request)

    def get_channel_by_name(self, channel_name: str) -> Dict:
        request = self.youtube.search().list(part="snippet", q=channel_name, type="channel")
        response = self._execute_request(request)
        channel_id = response["items"][0]["id"]["channelId"]
        return self.get_channel(channel_id)

    def get_video(self, video_id: str) -> Dict:
        request = self.youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
        return self._execute_request(request)

    def get_thumbnail(self, video: Dict, resolution: ThumbnailSize = ThumbnailSize.HIGH) -> str:
        return video["snippet"]["thumbnails"][resolution.value]["url"]

    def get_video_stats(self, video: Dict) -> Dict[str, int]:
        stats = video.get("statistics", {})
        return {
            "viewCount": int(stats.get("viewCount", 0)),
            "likeCount": int(stats.get("likeCount", 0)),
            "commentCount": int(stats.get("commentCount", 0)),
        }

    def get_top_videos(self, channel_id: str, num_videos: int = 50) -> List[Dict]:
        search_request = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=num_videos,
            order="viewCount",
            type="video",
        )
        search_response = self._execute_request(search_request)

        video_ids = [video["id"]["videoId"] for video in search_response.get("items", [])]
        if not video_ids:
            return []

        details_request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics", id=",".join(video_ids)
        )
        details_response = self._execute_request(details_request)
        return details_response["items"]

    def get_last_videos(self, channel_id: str, num_videos: int = 50) -> List[Dict]:
        request = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=num_videos,
            order="date",
            type="video",
        )
        response = self._execute_request(request)
        video_ids = [video["id"]["videoId"] for video in response.get("items", [])]
        if not video_ids:
            return []

        details_request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics", id=",".join(video_ids)
        )
        details_response = self._execute_request(details_request)
        return details_response["items"]

    def get_channel_thumbnail(
        self,
        channel: dict[str, Union[str, dict[str, str]]],
        resolution: Literal[
            ThumbnailSize.DEFAULT,
            ThumbnailSize.STANDARD,
            ThumbnailSize.MEDIUM,
            ThumbnailSize.HIGH,
        ] = ThumbnailSize.DEFAULT,
    ) -> str:
        """
        Retrieves the thumbnail of a channel
        """
        return channel["items"][0]["snippet"]["thumbnails"][resolution.value]["url"]

    def get_categories(self, region: str) -> Dict[str, str]:
        region_code_map = {"united_states": "US", "poland": "PL"}
        region_code = region_code_map.get(region, "US")
        request = self.youtube.videoCategories().list(part="snippet", regionCode=region_code)
        response = self._execute_request(request)
        return {item["id"]: item["snippet"]["title"] for item in response["items"]}


def show_thumbnail_from_url(url: str) -> None:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    plt.imshow(img)
    plt.axis("off")
    plt.show()
