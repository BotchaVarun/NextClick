"""
Cloudinary image upload helper.
Used instead of local disk storage because Render's filesystem is ephemeral -
anything saved to disk is wiped on every redeploy/restart.
"""
import cloudinary
import cloudinary.uploader
from flask import current_app


def init_cloudinary(app):
    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],
        secure=True,
    )


def upload_image(file_storage, folder="photography-business"):
    """
    Uploads a Werkzeug FileStorage object to Cloudinary.
    Returns the secure HTTPS URL, or None if no file was provided.
    """
    if not file_storage or not file_storage.filename:
        return None
    try:
        result = cloudinary.uploader.upload(
            file_storage,
            folder=folder,
            resource_type="image",
            overwrite=True,
        )
        return result.get("secure_url")
    except Exception as e:
        current_app.logger.error("Cloudinary upload failed: %s", e)
        return None


def delete_image(public_id):
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception as e:
        current_app.logger.error("Cloudinary delete failed: %s", e)
