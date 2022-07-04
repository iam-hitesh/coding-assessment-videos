from datetime import datetime, timedelta
import math

from django.conf import settings

import apiclient
from apiclient.discovery import build
from celery import shared_task

import app.models as models


@shared_task(name='fetch_youtube_videos', default_retry_delay=10 * 60)
def fetch_youtube_videos():
    api_keys = settings.GOOGLE_API_KEYS

    time_now = datetime.now()
    last_request_time = time_now - timedelta(minutes=5)

    valid = False

    # For handling multiple api keys
    for key in api_keys:
        try:
            youtube = build("youtube", "v3", developerKey=key)
            req_cricket = youtube.search().list(q="cricket", part="snippet",
                                                order="date", maxResults=50,
                                                publishedAfter=(
                                                            last_request_time.replace(microsecond=0).isoformat() + 'Z'))
            req_cricket = req_cricket.execute()

            current_results = req_cricket['items']
            total_available_results = req_cricket['totalResults']

            if total_available_results > 50:
                next_page_token = req_cricket['nextPageToken']
                results_left = total_available_results - 50

                for i in range(0, int(math.ceil((results_left/50) + 1))):
                    req_cricket = youtube.search().list(q="cricket", part="snippet",
                                                        nex="date", maxResults=50,
                                                        pageToken=next_page_token,
                                                        publishedAfter=(
                                                                last_request_time.replace(microsecond=0).isoformat() + 'Z'))
                    req_cricket = req_cricket.execute()

                    next_page_token = req_cricket['nextPageToken']
                    current_results += req_cricket['items']

            res = current_results

            valid = True
        except apiclient.errors.HttpError as err:
            print('-----------------')
            print(err)
            print('-----------------')

            code = err.resp.status
            if not (code == 400 or code == 403):
                break

        if valid:
            break

    if not valid:
        return False

    for item in res:
        video_id = item['id']['videoId']
        published_at = item['snippet']['publishedAt']
        title = item['snippet']['title']
        description = item['snippet']['description']
        thumbnails_urls = item['snippet']['thumbnails']['default']['url']
        channel_id = item['snippet']['channelId']
        channel_title = item['snippet']['channelTitle']

        models.Video.objects.create(
            video_id=video_id,
            title=title,
            description=description,
            channel_id=channel_id,
            channel_title=channel_title,
            published_at=published_at,
            thumbnails_urls=thumbnails_urls,
        )
