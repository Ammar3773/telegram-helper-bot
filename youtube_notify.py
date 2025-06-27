# youtube_notify.py

import requests
from config import YOUTUBE_API_KEY, YOUTUBE_CHANNEL_ID

last_video_id = None

def get_latest_video():
    global last_video_id

    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={YOUTUBE_CHANNEL_ID}&part=snippet,id&order=date&maxResults=1"
    response = requests.get(url).json()

    if "items" in response:
        video = response["items"][0]
        if video["id"]["kind"] == "youtube#video":
            video_id = video["id"]["videoId"]
            if video_id != last_video_id:
                last_video_id = video_id
                title = video["snippet"]["title"]
                link = f"https://youtu.be/{video_id}"
                return f"📢 *New Video Uploaded!*\n🎬 *{title}*\n🔗 {link}"
    return None
