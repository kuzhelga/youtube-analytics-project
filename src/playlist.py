import os
from googleapiclient.discovery import build
import datetime
import isodate


api_key: str = os.getenv('API_KEY')  # подтягивается API_KEY из системы


class PlayList:
    """Класс для получения плейлиста"""

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_data = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        self.title = self.playlist_data["items"][0]["snippet"]["title"]
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,).execute()
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_dict = self.youtube.videos().list(part='contentDetails,statistics',
                                                     id=','.join(self.video_ids)).execute()

    def __str__(self):
        return self.playlist_videos

    @property
    def total_duration(self):
        """Подсчет суммарной длительности плейлиста"""
        total_duration = datetime.timedelta()
        for video in self.video_dict['items']:
            duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        sorted_list = sorted(self.video_dict['items'], key=lambda x: int(x['statistics']['likeCount']), reverse=True)
        best_video_id = sorted_list[0]['id']
        return f"https://youtu.be/{best_video_id}"
