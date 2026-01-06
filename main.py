import json
import os
import time
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

VIDEO_IDS = [
    "YhN6kz9DvV4",
    "DmzmgrH4PJc",
    "hvJ786sjKFM"
]

PUBLIC_TIME = 30 * 60     # 30 minutes
UNLISTED_TIME = 90 * 60  # 90 minutes
TOTAL_DAYS = 30

def get_service():
    secret_json = json.loads(os.environ["CLIENT_SECRET_JSON"])
    creds = Credentials.from_authorized_user_info(secret_json, scopes=[
        "https://www.googleapis.com/auth/youtube.force-ssl"
    ])
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)

def set_visibility(youtube, video_id, status):
    youtube.videos().update(
        part="status",
        body={
            "id": video_id,
            "status": {"privacyStatus": status}
        }
    ).execute()
    print(f"{datetime.now()} → {video_id} set to {status}")

def main():
    youtube = get_service()
    end_time = datetime.now() + timedelta(days=TOTAL_DAYS)

    while datetime.now() < end_time:
        for vid in VIDEO_IDS:
            set_visibility(youtube, vid, "public")
            time.sleep(PUBLIC_TIME)

            set_visibility(youtube, vid, "unlisted")
            time.sleep(UNLISTED_TIME)

if __name__ == "__main__":
    main()
