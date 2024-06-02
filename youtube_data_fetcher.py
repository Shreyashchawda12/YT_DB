from googleapiclient.discovery import build
import pandas as pd
from logger import logger
import os

class YouTubeDataFetcher:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_trending_videos(self, region_code='US', max_results=50):
        trending_videos = []
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                chart='mostPopular',
                regionCode=region_code,
                maxResults=max_results
            )
            response = request.execute()
            
            for item in response['items']:
                video_id = item['id']
                title = item['snippet']['title']
                description = item['snippet']['description']
                published_at = item['snippet']['publishedAt']
                channel_title = item['snippet']['channelTitle']
                tags = item['snippet'].get('tags', [])
                view_count = item['statistics'].get('viewCount', 'N/A')
                like_count = item['statistics'].get('likeCount', 'N/A')
                dislike_count = item['statistics'].get('dislikeCount', 'N/A')
                comment_count = item['statistics'].get('commentCount', 'N/A')
                duration = item['contentDetails'].get('duration', 'N/A')
                dimension = item['contentDetails'].get('dimension', 'N/A')
                definition = item['contentDetails'].get('definition', 'N/A')
                caption = item['contentDetails'].get('caption', 'N/A')
                category_id = item['snippet'].get('categoryId', 'N/A')

                video_info = {
                    'Video ID': video_id,
                    'Title': title,
                    'Description': description,
                    'Published At': published_at,
                    'Channel Title': channel_title,
                    'Tags': tags,
                    'View Count': view_count,
                    'Like Count': like_count,
                    'Dislike Count': dislike_count,
                    'Comment Count': comment_count,
                    'Duration': duration,
                    'Dimension': dimension,
                    'Definition': definition,
                    'Caption': caption,
                    'Category ID': category_id,
                    'Region Code': region_code
                }
                trending_videos.append(video_info)
            logger.info(trending_videos)
                
        except Exception as e:
            logger.error(f"An error occurred while retrieving trending videos: {e}")
        
        return trending_videos

    def get_category_names(self):
        categories = {}
        try:
            request = self.youtube.videoCategories().list(
                part="snippet",
                regionCode='US'
            )
            response = request.execute()
            for item in response['items']:
                category_id = item['id']
                category_name = item['snippet']['title']
                categories[category_id] = category_name
            logger.info(categories)
        except Exception as e:
            logger.error(f"An error occurred while retrieving categories: {e}")
        return categories
