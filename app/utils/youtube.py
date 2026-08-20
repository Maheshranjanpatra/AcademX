import requests
from flask import current_app
import re

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"


def extract_playlist_id(url):
    """Extract playlist ID from a YouTube URL."""
    patterns = [
        r'list=([^&]+)',
        r'/playlist\?list=([^&]+)',
        r'youtu\.be\/.*\?list=([^&]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_video_id(url):
    """Extract video ID from a YouTube URL."""
    patterns = [
        r'v=([^&]+)',
        r'youtu\.be\/([^?]+)',
        r'/embed/([^?]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_playlist_videos(playlist_id, api_key=None):
    """Fetch all videos from a YouTube playlist using the Data API v3."""
    if not api_key:
        api_key = current_app.config.get('YOUTUBE_API_KEY')

    if not api_key:
        raise ValueError("YouTube API key not configured.")

    videos = []
    next_page_token = None

    while True:
        params = {
            'key': api_key,
            'playlistId': playlist_id,
            'part': 'snippet,contentDetails',
            'maxResults': 50,
        }
        if next_page_token:
            params['pageToken'] = next_page_token

        response = requests.get(f"{YOUTUBE_API_URL}/playlistItems", params=params)
        data = response.json()

        if 'items' not in data:
            break

        for item in data['items']:
            snippet = item.get('snippet', {})
            content_details = item.get('contentDetails', {})
            video_id = content_details.get('videoId')
            title = snippet.get('title', 'Untitled')
            description = snippet.get('description', '')
            thumbnail = snippet.get('thumbnails', {}).get('default', {}).get('url', '')

            duration_str = content_details.get('duration', 'PT0S')
            duration_seconds = parse_duration(duration_str)

            videos.append({
                'video_id': video_id,
                'title': title,
                'description': description,
                'thumbnail': thumbnail,
                'duration_seconds': duration_seconds,
                'embed_url': f"https://www.youtube-nocookie.com/embed/{video_id}",
                'watch_url': f"https://www.youtube.com/watch?v={video_id}",
            })

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return videos


def parse_duration(duration_str):
    """Convert ISO 8601 duration (PT1H2M3S) to seconds."""
    import re
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, duration_str)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def get_playlist_details(playlist_id, api_key=None):
    """Fetch playlist title and description."""
    if not api_key:
        api_key = current_app.config.get('YOUTUBE_API_KEY')

    params = {
        'key': api_key,
        'id': playlist_id,
        'part': 'snippet',
    }
    response = requests.get(f"{YOUTUBE_API_URL}/playlists", params=params)
    data = response.json()

    if 'items' in data and data['items']:
        snippet = data['items'][0].get('snippet', {})
        return {
            'title': snippet.get('title', 'Untitled Playlist'),
            'description': snippet.get('description', ''),
            'channel_title': snippet.get('channelTitle', ''),
        }
    return None
