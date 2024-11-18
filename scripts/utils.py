from dataclasses import dataclass


@dataclass
class Video:
    def __init__(
        self,
        video_id,
        title,
        description,
        category,
        thumbnail,
        author,
        author_id,
        views,
        likes,
        comments,
        date
    ):
        self.video_id = video_id
        self.title = title
        self.description = description
        self.category = category
        self.thumbnail = thumbnail
        self.author = author
        self.author_id = author_id
        self.views = views
        self.likes = likes
        self.comments = comments
        self.date = date

    def __str__(self):
        return f"{self.title} - {self.author}"


@dataclass
class Channel:
    def __init__(
        self,
        name,
        rank,
        id=None,
        thumbnail=None,
        description=None,
    ):
        self.name = name
        self.rank = rank
        self.id = id
        self.thumbnail = thumbnail
        self.description = description
