import os
import re
import json
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "UC6I30jm-TlamEB9H6kQMbdw"


def update_youtube():
    print("Checking YouTube...")

    with open("whatsnew.json", "r", encoding="utf-8") as f:
        current_data = json.load(f)

    base = "https://www.googleapis.com/youtube/v3"

    # Get the channel's uploads playlist
    channel = requests.get(
        f"{base}/channels",
        params={
            "part": "contentDetails",
            "id": CHANNEL_ID,
            "key": YOUTUBE_API_KEY
        }
    ).json()

    uploads_id = (
        channel["items"][0]
        ["contentDetails"]
        ["relatedPlaylists"]
        ["uploads"]
    )

    print("Uploads playlist:", uploads_id)

    # Get latest 3 videos
    playlist = requests.get(
        f"{base}/playlistItems",
        params={
            "part": "snippet",
            "playlistId": uploads_id,
            "maxResults": 3,
            "key": YOUTUBE_API_KEY
        }
    ).json()

    video_ids = [
        item["snippet"]["resourceId"]["videoId"]
        for item in playlist["items"]
    ]

    print("YouTube videos:", video_ids)

    current_ids = [
        video["videoId"]
        for video in current_data["whats_new"]
    ]

    print("Current videos:", current_ids)

    # If the IDs are exactly the same, nothing needs updating.
    if video_ids == current_ids:
        print("No new videos.")
        return current_data

    print("NEW VIDEO DETECTED!")

    # Get full information about the videos
    videos = requests.get(
        f"{base}/videos",
        params={
            "part": "snippet,contentDetails",
            "id": ",".join(video_ids),
            "key": YOUTUBE_API_KEY
        }
    ).json()["items"]

    new_data = {
        "whats_new": []
    }

    for i, video in enumerate(videos):

        snippet = video["snippet"]
        details = video["contentDetails"]

        match = re.search(
            r"PT(?:(\d+)M)?",
            details["duration"]
        )

        duration = (
            int(match.group(1) or 0)
            if match
            else 0
        )

        new_data["whats_new"].append({
            "id": i + 1,
            "title": snippet["title"],

            # Your fixed thumbnail
            "thumbnail": (
    snippet["thumbnails"].get("maxres", {}).get("url")
    or snippet["thumbnails"].get("high", {}).get("url")
    or snippet["thumbnails"].get("medium", {}).get("url")
),

            "videoId": video["id"],
            "videoSource": "youtube",
            "duration": duration,
            "publishedAt": snippet["publishedAt"][:10]
        })

    # Save it
    with open("whatsnew.json", "w", encoding="utf-8") as f:
        json.dump(
            new_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("whatsnew.json UPDATED!")

    return new_data