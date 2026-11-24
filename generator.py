"""
Streaming Video Events Generator
--------------------------------
Simulates real-time streaming video user activity (PLAY, PAUSE, BUFFERING, etc.)
and continuously outputs records as JSON lines into a local data lake folder.
"""

import os
import json
import time
import uuid
import random
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
OUTPUT_DIR = "Local_Data_Lake"
SLEEP_INTERVAL_SEC = 1.0  # Delay between generated events (seconds)
MAX_CONCURRENT_SESSIONS = 15

# AWS S3 Cloud Configuration (Optional: set here or via environment variables)
S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET", "")  # e.g., "prime-video-telemetry-lake-yourname"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)

# Movie Catalog
MOVIES = [
    {"movie_id": "mov_001", "title": "The Matrix", "duration_sec": 8160, "genre": "Sci-Fi"},
    {"movie_id": "mov_002", "title": "Inception", "duration_sec": 8880, "genre": "Sci-Fi"},
    {"movie_id": "mov_003", "title": "The Dark Knight", "duration_sec": 9120, "genre": "Action"},
    {"movie_id": "mov_004", "title": "Interstellar", "duration_sec": 10140, "genre": "Sci-Fi"},
    {"movie_id": "mov_005", "title": "Pulp Fiction", "duration_sec": 9240, "genre": "Crime"},
    {"movie_id": "mov_006", "title": "Gladiator", "duration_sec": 9300, "genre": "Drama"},
    {"movie_id": "mov_007", "title": "Parasite", "duration_sec": 7920, "genre": "Thriller"},
    {"movie_id": "mov_008", "title": "Spirited Away", "duration_sec": 7500, "genre": "Animation"},
    {"movie_id": "mov_009", "title": "The Godfather", "duration_sec": 10500, "genre": "Crime"},
    {"movie_id": "mov_010", "title": "Avengers: Endgame", "duration_sec": 10860, "genre": "Action"},
]

USERS = [f"usr_{i:04d}" for i in range(1, 51)]

DEVICES = [
    {"type": "SmartTV", "os": "Tizen"},
    {"type": "SmartTV", "os": "webOS"},
    {"type": "Mobile", "os": "iOS"},
    {"type": "Mobile", "os": "Android"},
    {"type": "Tablet", "os": "iPadOS"},
    {"type": "Desktop", "os": "Windows"},
    {"type": "Desktop", "os": "macOS"},
    {"type": "StreamingStick", "os": "FireOS"},
]

RESOLUTIONS = ["4K", "1080p", "720p", "480p"]
COUNTRIES = ["US", "CA", "GB", "IN", "DE", "FR", "JP", "BR", "AU"]

# ---------------------------------------------------------
# State Management
# ---------------------------------------------------------
active_sessions = {}


def start_new_session():
    """Initializes a new viewing session."""
    session_id = str(uuid.uuid4())
    user_id = random.choice(USERS)
    movie = random.choice(MOVIES)
    device = random.choice(DEVICES)
    country = random.choice(COUNTRIES)
    resolution = random.choice(RESOLUTIONS)

    session = {
        "session_id": session_id,
        "user_id": user_id,
        "movie_id": movie["movie_id"],
        "movie_title": movie["title"],
        "genre": movie["genre"],
        "duration_sec": movie["duration_sec"],
        "device_type": device["type"],
        "device_os": device["os"],
        "country": country,
        "resolution": resolution,
        "current_position_sec": 0,
        "status": "PLAYING",
    }
    active_sessions[session_id] = session
    return session, "PLAY"


def advance_session(session_id):
    """Advances state for an active viewing session."""
    session = active_sessions[session_id]
    current_status = session["status"]
    duration = session["duration_sec"]

    if current_status == "PLAYING":
        # Increment watch position
        advance_by = random.randint(15, 60)
        session["current_position_sec"] = min(session["current_position_sec"] + advance_by, duration)

        if session["current_position_sec"] >= duration:
            event_type = "STOP"
            session["status"] = "ENDED"
        else:
            # Transition probability
            rand = random.random()
            if rand < 0.70:
                event_type = "PLAY"
            elif rand < 0.82:
                event_type = "BUFFERING"
                session["status"] = "BUFFERING"
            elif rand < 0.94:
                event_type = "PAUSE"
                session["status"] = "PAUSED"
            elif rand < 0.98:
                event_type = "SEEK"
                session["current_position_sec"] = random.randint(0, duration)
            else:
                event_type = "STOP"
                session["status"] = "ENDED"

    elif current_status == "PAUSED":
        rand = random.random()
        if rand < 0.75:
            event_type = "RESUME"
            session["status"] = "PLAYING"
        elif rand < 0.90:
            event_type = "PAUSE"
        else:
            event_type = "STOP"
            session["status"] = "ENDED"

    elif current_status == "BUFFERING":
        rand = random.random()
        if rand < 0.70:
            event_type = "RESUME"
            session["status"] = "PLAYING"
        elif rand < 0.90:
            event_type = "BUFFERING"
        elif rand < 0.96:
            event_type = "ERROR"
            session["status"] = "ENDED"
        else:
            event_type = "STOP"
            session["status"] = "ENDED"
    else:
        event_type = "STOP"

    return session, event_type


def generate_event():
    """Generates a single streaming event record."""
    if len(active_sessions) < MAX_CONCURRENT_SESSIONS and (not active_sessions or random.random() < 0.35):
        session, event_type = start_new_session()
    else:
        session_id = random.choice(list(active_sessions.keys()))
        session, event_type = advance_session(session_id)

    # Calculate bitrate based on resolution and event
    bitrate_map = {"4K": 15000, "1080p": 5000, "720p": 2500, "480p": 1000}
    base_bitrate = bitrate_map.get(session["resolution"], 3000)
    jitter = random.randint(-200, 200)
    bitrate = max(200, base_bitrate + jitter)

    if event_type == "BUFFERING":
        bitrate = int(bitrate * 0.3)

    event = {
        "event_id": str(uuid.uuid4()),
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "session_id": session["session_id"],
        "user_id": session["user_id"],
        "movie_id": session["movie_id"],
        "movie_title": session["movie_title"],
        "genre": session["genre"],
        "playback_position_sec": session["current_position_sec"],
        "movie_duration_sec": session["duration_sec"],
        "device_type": session["device_type"],
        "device_os": session["device_os"],
        "resolution": session["resolution"],
        "bitrate_kbps": bitrate,
        "country": session["country"],
    }

    if session["status"] == "ENDED" and session["session_id"] in active_sessions:
        del active_sessions[session["session_id"]]

    return event


def get_output_filepath():
    """Returns the daily partitioned JSON lines filepath."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return os.path.join(OUTPUT_DIR, f"streaming_events_{today}.jsonl")


RAW_LOGS_FILEPATH = os.path.join(OUTPUT_DIR, "raw_streaming_logs.jsonl")


def init_s3_client():
    """Initializes and returns a boto3 S3 client if configured."""
    if not S3_BUCKET_NAME:
        return None
    try:
        import boto3
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            client = boto3.client(
                "s3",
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
        else:
            client = boto3.client("s3", region_name=AWS_REGION)
        return client
    except Exception as e:
        print(f"⚠️ S3 Initialization Warning: {e}. Falling back to local mode.")
        return None


def upload_event_to_s3(s3_client, event):
    """Uploads a single JSON event to S3 partitioned by date."""
    try:
        now = datetime.now(timezone.utc)
        s3_key = (
            f"raw-telemetry/"
            f"year={now.year}/month={now.month:02d}/day={now.day:02d}/"
            f"{event['event_id']}.json"
        )
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(event),
            ContentType="application/json",
        )
        return True
    except Exception as e:
        print(f"⚠️ S3 Upload Error: {e}")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    s3_client = init_s3_client()

    print("=" * 70)
    print("Streaming Video Events Generator Started")
    print(f"Local output : {os.path.abspath(OUTPUT_DIR)}")
    if s3_client and S3_BUCKET_NAME:
        print(f"AWS S3 Cloud : Enabled -> s3://{S3_BUCKET_NAME}/raw-telemetry/")
    else:
        print("AWS S3 Cloud : Disabled (Set S3_BUCKET_NAME to stream to AWS S3)")
    print(f"Interval     : {SLEEP_INTERVAL_SEC} second(s)")
    print("Press Ctrl+C to stop.")
    print("=" * 70)

    event_count = 0
    s3_upload_count = 0

    try:
        while True:
            event = generate_event()
            filepath = get_output_filepath()

            # Append as JSON line
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
                f.flush()

            # Also append to raw_streaming_logs.jsonl in custom pipe-delimited format
            formatted_log = (
                f"[{event['event_timestamp']}] "
                f"User: {event['user_id']} | "
                f"Event: {event['event_type']} | "
                f"Movie: {event['movie_title']} | "
                f"Pos: {event['playback_position_sec']}s / {event['movie_duration_sec']}s\n"
            )
            with open(RAW_LOGS_FILEPATH, "a", encoding="utf-8") as f_raw:
                f_raw.write(formatted_log)
                f_raw.flush()

            # If S3 is configured, stream to AWS
            if s3_client:
                if upload_event_to_s3(s3_client, event):
                    s3_upload_count += 1

            event_count += 1
            cloud_tag = " [☁️ S3]" if s3_client else ""
            print(f"{formatted_log.strip()}{cloud_tag}")

            time.sleep(SLEEP_INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\n" + "-" * 70)
        print(f"Generator stopped by user. Total events generated: {event_count}")
        if s3_client:
            print(f"Total events uploaded to S3: {s3_upload_count}")
        print(f"Local data saved in '{OUTPUT_DIR}'.")
        print("-" * 70)


if __name__ == "__main__":
    main()

