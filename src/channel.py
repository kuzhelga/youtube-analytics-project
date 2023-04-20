import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')  # подтягивается API_KEY из системы
youtube = build('youtube', 'v3', developerKey=api_key)  # создается специальный объект для работы с API


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = youtube.channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.view_count = channel["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self):
        """Геттер для запрета изменения вывода ID канала"""
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        youtube_object = build('youtube', 'v3', developerKey=api_key)
        return youtube_object

    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра"""
        attributes = {
        'channel_id': self.__channel_id,
        'title': self.title,
        'description': self.description,
        'url': self.url,
        'subscriber_count': self.subscriber_count,
        'video_count': self.video_count,
        'view_count': self.view_count
        }

        with open(filename, 'w') as file:
            json.dump(attributes, file, ensure_ascii=False, indent="")

    def __str__(self):
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        """Метод для сложения подписчиков каналов"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Метод для сложения подписчиков каналов"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        """Метод для сравнения < (меньше)"""
        return int(self.subscriber_count) < int(other.subscriber_count)

