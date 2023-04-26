import os
from googleapiclient.discovery import build


class Video:
    """Класс для получения видео по ID"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = self.youtube.videos().list(part="snippet,statistics, contentDetails,topicDetails", id=video_id).execute()
        self.title = self.video_response["items"][0]["snippet"]["title"]   # Название видео
        self.url = f"https://www.youtu.be/{self.video_id}"  # Ссылка на видео
        self.view_count = self.video_response["items"][0]["statistics"]["viewCount"]    # Кол-во просмотров
        self.like_count = self.video_response["items"][0]["statistics"]["likeCount"]    # Кол-во лайков

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    """Класс наследует от класса Video, инициализирует ID видео и плейлиста"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return super().__str__()
