"""
Cloudinary Data Lake Uploader
-----------------------------
Uploads raw telemetry logs, database files, and visualization reports
to Cloudinary storage using the 'raw' resource type.
"""

import os
import glob
import cloudinary
import cloudinary.uploader
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ---------------------------------------------------------
# Cloudinary Configuration
# ---------------------------------------------------------
CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "pqspfq9j")
API_KEY = os.getenv("CLOUDINARY_API_KEY", "392223737612368")
API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

# Or pass full CLOUDINARY_URL: cloudinary://<api_key>:<api_secret>@<cloud_name>
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL", "")


def init_cloudinary():
    """Initializes Cloudinary SDK."""
    if CLOUDINARY_URL:
        cloudinary.config(cloudinary_url=CLOUDINARY_URL)
        return True
    elif CLOUD_NAME and API_KEY and API_SECRET:
        cloudinary.config(
            cloud_name=CLOUD_NAME,
            api_key=API_KEY,
            api_secret=API_SECRET,
            secure=True,
        )
        return True
    else:
        return False


def upload_file_to_cloudinary(local_filepath, remote_folder="prime_video_telemetry"):
    """Uploads a single file to Cloudinary as raw or image asset."""
    if not os.path.exists(local_filepath):
        print(f"❌ File not found: {local_filepath}")
        return None

    filename = os.path.basename(local_filepath)
    ext = os.path.splitext(filename)[1].lower()
    resource_type = "image" if ext in [".png", ".jpg", ".jpeg", ".webp"] else "raw"
    public_id = f"{remote_folder}/{filename}"

    print(f"⬆️ Uploading {local_filepath} as {resource_type} to Cloudinary...")
    try:
        response = cloudinary.uploader.upload(
            local_filepath,
            resource_type=resource_type,
            public_id=public_id,
            overwrite=True,
            use_filename=True,
            unique_filename=False,
        )
        url = response.get("secure_url", response.get("url"))
        print(f"✅ Successfully uploaded: {filename}")
        print(f"🔗 Cloudinary URL: {url}")
        return response
    except Exception as e:
        print(f"❌ Upload failed for {filename}: {e}")
        return None


def sync_all_telemetry():
    """Syncs all files in Local_Data_Lake to Cloudinary."""
    if not init_cloudinary():
        print("⚠️ Cloudinary credentials not configured.")
        print("Please set CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET in cloudinary_sync.py or your environment.")
        return

    data_lake_dir = "Local_Data_Lake"
    if not os.path.exists(data_lake_dir):
        print(f"❌ Local data lake folder '{data_lake_dir}' not found.")
        return

    files_to_sync = glob.glob(os.path.join(data_lake_dir, "*"))
    if not files_to_sync:
        print("ℹ️ No files found in Local_Data_Lake to upload.")
        return

    print("=" * 65)
    print(f"🚀 Cloudinary Data Lake Sync Started ({len(files_to_sync)} files found)")
    print("=" * 65)

    for filepath in files_to_sync:
        if os.path.isfile(filepath):
            upload_file_to_cloudinary(filepath)
            print("-" * 65)

    print("✨ Sync to Cloudinary complete!")


if __name__ == "__main__":
    sync_all_telemetry()

