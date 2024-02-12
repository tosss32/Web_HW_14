import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()
cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

def upload_image(file):

    cloudinary.config(
        cloud_name = cloud_name,
        api_key = api_key,
        api_secret = api_secret
    )

    result = cloudinary.uploader.upload(file, folder="avatars")

    return result["public_id"]




