import pandas as pd
from youtube_data_fetcher import YouTubeDataFetcher
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Replace with your own API key
api_key = os.getenv('YOUTUBE_API_KEY')

if not api_key:
    raise ValueError("API key not found. Please set the YOUTUBE_API_KEY environment variable.")

if __name__ == "__main__":
    # Create YouTubeDataFetcher instance
    fetcher = YouTubeDataFetcher(api_key)
    
    # Top 5 countries (region codes)
    top_countries = ['US', 'IN', 'BR', 'JP', 'GB']  # United States, India, Brazil, Japan, United Kingdom

    all_trending_videos = []

    # Fetch trending videos for each country
    for country in top_countries:
        trending_videos = fetcher.get_trending_videos(region_code=country, max_results=50)
        for video in trending_videos:
            video['Country'] = country  # Add country information
        all_trending_videos.extend(trending_videos)

    # Fetch category names
    categories = fetcher.get_category_names()
    
    # Convert category ID to category name
    for video in all_trending_videos:
        category_id = video.get('Category ID')
        if category_id in categories:
            video['Category Name'] = categories[category_id]

    # Save trending videos to CSV
    df = pd.DataFrame(all_trending_videos)
    df.to_csv('trending_videos_top_countries.csv', index=False)
    print("Trending videos with categories and countries saved to trending_videos_top_countries.csv")

    # Analysis example: Get trending categories
    category_counts = df['Category Name'].value_counts()
    print("Trending categories across top 5 countries:")
    print(category_counts)
